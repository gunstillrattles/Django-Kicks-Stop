from django.contrib import admin
from .models import *
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'size', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'category')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Category)
admin.site.register(Product)