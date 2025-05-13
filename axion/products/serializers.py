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
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
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
            "category",  # para GET
            "category_id",  # para POST/PUT
            "image_url",
            "rating",
            "attributes",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not request or not obj.image_url:
            return []
        paths = [p.strip() for p in obj.image_url.split(",") if p.strip()]
        return [request.build_absolute_uri(f"/media/{p}") for p in paths]
