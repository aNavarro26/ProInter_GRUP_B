from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_list_create, name="cart-list-create"),
    path("<int:cart_id>/", views.cart_detail, name="cart-detail"),
    path(
        "<int:cart_id>/items/",
        views.cart_items_list_create,
        name="cart-items-list-create",
    ),
    path(
        "<int:cart_id>/items/<int:cart_item_id>/",
        views.cart_item_detail,
        name="cart-item-detail",
    ),
]
