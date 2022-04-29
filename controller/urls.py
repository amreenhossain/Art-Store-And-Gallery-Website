from django.urls import path
from controller import views

app_name = 'controller'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product-details'),
    path('collection/', views.ProductView.as_view(), name='collection'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart-view/', views.cart_view, name='cart'),
    path('remove-item/<int:pk>/', views.remove_item_from_cart, name='remove-item'),
    path('checkout/', views.CheckoutTemplateView.as_view(), name='checkout'),
    path('gallery/', views.GalleryListView.as_view(), name='gallery'),
]