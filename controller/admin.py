from django.contrib import admin
from controller.models import Profile, Category, Product, Order, Cart, BillingAddress, Banner


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(Banner)


