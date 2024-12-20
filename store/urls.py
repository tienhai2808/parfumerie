from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('account/register/', register, name='register'),
    path('account/login/', login, name='login'),
    path('account/logout/', logout, name='logout'),
    path('account/', account, name='account'),
    path('perfumes/<slug:slug_pro>/', product_detail, name='product-detail'),
    path('cart/', cart, name='cart'),
    path('search/', search, name='search'),
    path('contact/', contact, name='contact'),
    path('<slug:slug_cat>/', category, name='category'),
    path('checkout/success/', checkout_success, name='checkout-success'),
    path('checkout/<str:username>/', checkout, name='checkout'),
    path('account/ordered/<int:id_order>/', order_detail, name='order-detail'),
] 