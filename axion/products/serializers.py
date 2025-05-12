from rest_framework import serializers
from .models import Category, Product, Attribute, ProductAttribute


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "name"]


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["attribute_id", "name"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ["product_attribute_id", "attribute", "value"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    attributes = ProductAttributeSerializer(
        source="productattribute_set", many=True, read_only=True
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "product_id",
            "name",
            "description",
            "price",
            "stock",
            "series",
            "image_url",
            "rating",
            "category",
            "attributes",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not request:
            return []
        paths = obj.image_url.split(",")
        return [request.build_absolute_uri(f"/media/{p.strip()}") for p in paths]
