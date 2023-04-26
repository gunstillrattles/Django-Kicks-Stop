from django.db import models
from django.contrib.auth.models import User
class Product(models.Model):
	name = models.CharField(max_length=200, verbose_name="Название кроссовок")
	price = models.FloatField(verbose_name="Цена")
	image = models.ImageField(null=True, blank=True, upload_to="images/")
	def __str__(self):
		return self.name

@property
def imageURL(self):
	try:
		url = self.image.url
	except:
		url = ''
	return url
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Пользователь")
	name = models.CharField(max_length=200, null=True, verbose_name="Имя пользователя")
	email = models.CharField(max_length=200, verbose_name="Почта пользователя")
	def __str__(self):
		return self.name

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping
	@property
	def get_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Продукт который был заказан(ID)")
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name="ID заказа")
	quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name="Количество")
	date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь которому нужно доставить(ID)")
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name="ID заказа")
	address = models.CharField(max_length=200, null=False, verbose_name="Адрес заказчика")
	city = models.CharField(max_length=200, null=False, verbose_name="Город заказчика")
	zipcode = models.CharField(max_length=200, null=False, verbose_name="Зипкод заказчика")
	date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
	def __str__(self):
		return self.address