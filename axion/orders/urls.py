from django.urls import path
from .views import (
    order_list,
    order_user_list,
    order_detail,
    order_items_list,
    order_item_detail,
    shipment_detail,
    shipment_list,
    update_order_status,
    process_checkout,
)

urlpatterns = [
    path("", order_list, name="order-list"),
    path("user/<int:user_id>/", order_user_list, name="order-user-list"),
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
    path("<int:order_id>/status/", update_order_status, name="order-update-status"),
    path("checkout/", process_checkout, name="process-checkout"),
]
