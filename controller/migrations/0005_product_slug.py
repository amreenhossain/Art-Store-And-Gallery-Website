# Generated by Django 4.0.3 on 2022-04-14 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0004_remove_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='test'),
            preserve_default=False,
        ),
    ]