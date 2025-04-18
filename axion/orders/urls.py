from django.urls import path
from .views import (
    order_list,
    order_detail,
    order_items_list,
    order_item_detail,
    shipment_detail,
    shipment_list,
)

urlpatterns = [
    path("", order_list, name="order-list"),
    path("<int:pk>/", order_detail, name="order-detail"),
    path("<int:order_id>/items/", order_items_list, name="order-items-list"),
    path(
        "<int:order_id>/items/<int:order_item_id>/",
        order_item_detail,
        name="order-item-detail",
    ),
    path("<int:order_id>/shipments/", shipment_list, name="shipment-list"),
    path(
        "<int:order_id>/shipments/<int:shipment_id>/",
        shipment_detail,
        name="shipment-detail",
    ),
]
