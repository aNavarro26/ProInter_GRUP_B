from rest_framework import serializers
from .models import Order, OrderItem, Shipment


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["order_item_id", "order", "product", "quantity", "price", "subtotal"]
        extra_kwargs = {"order": {"required": False}}


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ["shipment_id", "order", "shipment_date"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipments = ShipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["order_id", "customer", "order_date", "status", "items", "shipments"]
