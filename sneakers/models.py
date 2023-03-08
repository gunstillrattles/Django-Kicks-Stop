from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название кроссовок")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    size = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Размер обуви")
    description = models.TextField(max_length=366, verbose_name="Описание")
    image_name = models.CharField(max_length=100, verbose_name="Название картинки")