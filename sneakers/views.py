from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import datetime

from django.views import View

from .forms import LoginForm
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.template import loader

class LoginView(View):
	form_class = LoginForm

	def post(self, req, *args, **kwargs):
		form = self.form_class(data=req.POST)

		if form.is_valid():
			pass
		else:
			return HttpResponse("The form is not valid!")
	def	get(self,req,*args,**kwargs):
		form = self.form_class()
		return render(
			req, "login.html",
			{
				"form": form,
			},
		)

class LogoutView(View):
	def	get(self,req,*args,**kwargs):
		return HttpResponse("Logout view")

def mainpage(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products': products, 'cartItems': cartItems}
	return render(request, 'mainpage.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'cart.html', context)


def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)
def about(request):
    contact_list = Product.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'about.html', {'page_obj': page_obj, 'title': 'О сайте'})


def pageNotFound(request, exception):
    template = loader.get_template('404.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponseNotFound(rendered_page)

def pageBadRequest(request, exception):
    template = loader.get_template('400.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponseBadRequest(rendered_page)

def pageForbidden(request, exception):
    template = loader.get_template('403.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponseForbidden(rendered_page)
