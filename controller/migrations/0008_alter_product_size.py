# Generated by Django 4.0.3 on 2022-04-14 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0007_alter_product_artist_alter_product_medium_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(max_length=150, verbose_name='size'),
        ),
    ]
