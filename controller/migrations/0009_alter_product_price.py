# Generated by Django 4.0.3 on 2022-04-14 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0008_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(max_length=180, verbose_name='Price'),
        ),
    ]
