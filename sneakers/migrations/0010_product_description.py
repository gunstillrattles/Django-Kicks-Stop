# Generated by Django 4.1.6 on 2023-04-27 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0009_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default=0, max_length=200, verbose_name='Описание'),
            preserve_default=False,
        ),
    ]
