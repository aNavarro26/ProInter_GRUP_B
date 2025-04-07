from django.contrib import admin
from django.urls import path
from .views import cart_item_list_create, cart_detail,cart_item_detail
urlpatterns = [
    path('cart/', cart_item_list_create, name='cart-list-create'),
    path('cart/<int:cart_id>/', cart_detail, name='cart-detail'),
    path('cart-items/', cart_item_list_create, name='cart-item-list-create'),
    path('cart-items/<int:cart_item_id>/', cart_item_detail, name='cart-item-detail'),

]
