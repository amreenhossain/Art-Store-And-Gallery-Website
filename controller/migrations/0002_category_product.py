# Generated by Django 4.0.3 on 2022-04-13 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='controller.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('preview_des', models.CharField(max_length=255, verbose_name='Short Descriptions')),
                ('description', models.TextField(max_length=1000, verbose_name='Descriptions')),
                ('image', models.ImageField(default='demo/demo.jpg', upload_to='products')),
                ('price', models.FloatField()),
                ('old_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('is_stock', models.BooleanField(default=True)),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='controller.category')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]