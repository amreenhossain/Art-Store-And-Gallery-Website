from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse

from controller.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate 
from django.views.generic import ListView, DetailView
from django.contrib import messages
from controller.models import Category, Product, Cart, Order 

def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            return redirect('controller:index')
        else:
            order.orderitems.add(order_item[0])
            return redirect('controller:index')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        return redirect('controller:index')

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
        return redirect('controller:login')
    
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