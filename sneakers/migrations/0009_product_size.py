# Generated by Django 4.1.6 on 2023-04-27 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0008_remove_product_vat'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.FloatField(default=42, verbose_name='Размер'),
            preserve_default=False,
        ),
    ]
