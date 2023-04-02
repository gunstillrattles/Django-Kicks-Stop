from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path("login/", views.LoginView.as_view(), name="login", ),
    path("logout/", views.LogoutView.as_view(), name="logout", ),
    path('about/', views.about, name='about'),
]