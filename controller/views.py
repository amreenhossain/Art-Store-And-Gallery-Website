from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from controller.forms import ProfileForm, RegistrationForm, BillingAddressForm, PaymentMethodForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate 
from django.views.generic import ListView, DetailView
from django.contrib import messages
from controller.models import Profile, Category, Product, Cart, Order, BillingAddress, Banner
from django.views.generic import TemplateView


class CheckoutTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0] 
        form = BillingAddressForm(instance=saved_address)
        payment_method = PaymentMethodForm()
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        order_item = order_qs[0].orderitems.all()
        order_total = order_qs[0].get_totals()

        context = {
        'billing_address': form, 
        'order_item': order_item,
        'order_total': order_total,
        'payment_method': payment_method,
        }
        return render(request, 'checkout.html', context)

    def post(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0] 
        form = BillingAddressForm(instance=saved_address)
        payment_obj = Order.objects.filter(user=request.user, ordered=False)[0]
        payment_form = PaymentMethodForm(instance=payment_obj)
        if request.method == 'post' or request.method == 'POST':
            form = BillingAddressForm(request.POST, instance=saved_address)
            pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
            if form.is_valid() and pay_form.is_valid():
                form.save()
                pay_method = pay_form.save()
               

                if not saved_address.is_fully_filled():
                    return redirect('controller:checkout')

                if pay_method.payment_method == 'Cash on Delivery':
                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order = order_qs[0]
                    order.ordered = True
                    order.orderId = order.id
                    order.paymentId = pay_method.payment_method
                    order.save()
                    cart_items = Cart.objects.filter(user=request.user, purchased=False)
                    for item in cart_items:
                        item.purchased = True
                        item.save()
                    print('Order Submited Successsfully')
                    return redirect('controller:index')

def add_to_cart(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Product, pk=pk)
        order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item[0].quantity += 1
                order_item[0].save()
                return redirect('controller:collection')
            else:
                order.orderitems.add(order_item[0])
                return redirect('controller:collection')
        else:
            order = Order(user=request.user)
            order.save()
            order.orderitems.add(order_item[0])
            return redirect('controller:collection')
    else:
        return redirect('controller:user_login')

def cart_view(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {
                'carts': carts,
                'order': order
            }
            return render(request, 'cart.html', context)
        else:
          return redirect('controller:index')  
    else:
        return redirect('controller:user_login')
    
def remove_item_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            return redirect('controller:cart')
        else:
            return redirect('controller:cart')
    else:
        return redirect('controller:cart')




class IndexListView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

  
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'item'
    
class ProductView(ListView):
    model = Product
    template_name = 'collection.html'
    context_object_name = 'products'

class GalleryListView(ListView):
    model = Product
    template_name = 'gallery.html'
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context ['banners'] = Banner.objects.filter(is_active=True).order_by('-id')
        return context



# def product_details(request, pk):
#     item = Product.objects.get(id=pk)
#     context = {
#         'item': item 
#     }
#     return render(request, 'store/product.html', context)

def user_register(request):
    if request.user.is_authenticated:
        return redirect('/')
        return 
    else:
        form = RegistrationForm()
        if request.method == 'post' or request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST' or request.method == 'post':
            username = request.POST.get('username')
            password = request.POST.get('password')
            customer = authenticate(request, username=username, password=password)
            if customer is not None:
                login(request, customer)
                return redirect('/')
            else:
                return redirect('controller:user_login')
                

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')


class ProfileView(TemplateView):
    
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user, ordered=True)
        billingaddress = BillingAddress.objects.get(user=request.user)
        billingaddress_form = BillingAddressForm(instance=billingaddress)
        profile_obj = Profile.objects.get(user=request.user)
        profileForm = ProfileForm(instance=profile_obj)

        context = {
            'orders': orders,
            'billingaddress': billingaddress_form,
            'profileForm': profileForm
        }
        return render(request, 'profile.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'post' or request.method == 'POST':
            billingaddress = BillingAddress.objects.get(user=request.user)
            billingaddress_form = BillingAddressForm(request.POST, instance=billingaddress)
            profile_obj = Profile.objects.get(user=request.user)
            profileForm = ProfileForm(request.POST, instance=profile_obj)
            if billingaddress_form.is_valid() or profileForm.is_valid():
                billingaddress_form.save()
                profileForm.save()
                return redirect('controller:profile')

    