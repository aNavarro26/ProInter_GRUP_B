from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source="product"
    )

    class Meta:
        model = CartItem
        fields = [
            "cart",
            "cart_item_id",
            "product",
            "product_id",
            "quantity",
            "price",
            "subtotal",
        ]
        read_only_fields = ["price", "subtotal"]

    def create(self, validated_data):
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")

        validated_data["price"] = product.price
        validated_data["subtotal"] = product.price * quantity

        return super().create(validated_data)

    def update(self, instance, validated_data):
        quantity = validated_data.get("quantity", instance.quantity)
        instance.quantity = quantity
        instance.price = instance.product.price
        instance.subtotal = instance.price * quantity
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["cart_id", "customer", "items"]
