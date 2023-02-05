from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('sneaker/<slug:sneakerid>', sneaker),
    path('sneakers/', sneakers),
]