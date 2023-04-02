from django.views.generic import TemplateView
from .models import Product
from .utils import cartData

class DataMixin:
    def get_context_data(self, **kwargs):
        data = cartData(self.request)
        cartItems = data['cartItems']
        context = super().get_context_data(**kwargs)
        context.update({
            'cartItems': cartItems,
            'products': Product.objects.all()
        })
        return context

class MainPageView(DataMixin, TemplateView):
    template_name = 'mainpage.html'

