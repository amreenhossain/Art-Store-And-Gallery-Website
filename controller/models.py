from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from django.contrib.auth.models import User
from django.template.defaultfilters import default, slugify
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=100, blank=False, null=False)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=300, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        user_email = self.user.email
        split_username = user_email.index('@')
        get_username = user_email[:split_username]
        self.username = get_username
        return super().save(*args, **kwargs)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    image = models.ImageField(upload_to='category', blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category') 
    artist = models.CharField(max_length=180, verbose_name='Artist')
    medium = models.CharField(max_length=180, verbose_name='Medium')
    size = models.CharField(max_length=150, verbose_name='size')
    description = models.TextField(max_length=1000, verbose_name='Descriptions')
    image = models.ImageField(upload_to='products', default='demo/demo.jpg', blank=False, null=False)
    price = models.FloatField()
    old_price = models.FloatField(default=0.00, blank=True, null=True)
    is_stock = models.BooleanField(default=True)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']

    def get_product_url(self):
        return reverse('controller:product-details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} X {self.item}"

    def get_total(self):
        total = self.item.price * self.quantity
        
        float_total = format(total, '0.2f')
        return float_total

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=255, blank=True, null=True)
    orderId = models.CharField(max_length=255, blank=True, null=True)
    

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
                total += float(order_item.get_total())
        return total