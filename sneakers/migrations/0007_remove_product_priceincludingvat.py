# Generated by Django 4.1.6 on 2023-04-27 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0006_product_vat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='priceIncludingVAT',
        ),
    ]
