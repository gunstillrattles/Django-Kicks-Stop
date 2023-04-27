from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.views import View
from django.contrib.auth.models import User
from .forms import LoginForm, CreateUserForm
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.template import loader
from django.contrib import messages
from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import ProductSerializer

class LoginView(View):
	form_class = LoginForm

	def post(self, req, *args, **kwargs):
		form = self.form_class(data=req.POST)

		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]

			user = authenticate(req, username=username, password=password,)

			if user is not None:
				login(req, user)
				return redirect('mainpage')
			else:
				return HttpResponse("You couldn't login ")

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
		user = req.user
		if isinstance(user, AnonymousUser):
			return HttpResponse("You haven't even logged in yet!")
		else:
			logout(req)
			return redirect('mainpage')


def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			Customer.objects.create(user=user, name=user.username, email=user.email)
			messages.success(request, 'Account created')
			return redirect('login')

	context = {'form':form}
	return render(request, 'register.html', context)

def mainpage(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products': products, 'cartItems': cartItems}
	return render(request, 'mainpage.html', context)
def detail_page(request,id):
	product=get_object_or_404(Product,pk=id)
	return render(request, 'detail.html',{'product':product})
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

class SneakerAPIList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )


class SneakerAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)


class SneakerAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly, )