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
    items_data = OrderItemSerializer(
        many=True,
        write_only=True,
        source="items",
    )

    shipments = ShipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "order_id",
            "customer",
            "order_date",
            "status",
            "items",
            "shipments",
            "items_data",
        ]
        extra_kwargs = {
            "order_date": {"required": False},
        }

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        order = Order.objects.create(**validated_data)

        for item in items_data:
            product = item.pop("product")
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=item["price"],
                subtotal=item["subtotal"],
            )

        return order
