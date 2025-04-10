from rest_framework import serializers
from .models import Category, Product, Attribute, ProductAttribute

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name']

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['attribute_id', 'name']

class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)
    
    class Meta:
        model = ProductAttribute
        fields = ['product_attribute_id', 'attribute', 'value']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    attributes = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'product_id',
            'name',
            'description',
            'price',
            'stock',
            'series',
            'category',
            'attributes'
        ]
    
    def get_attributes(self, obj):
        product_attrs = ProductAttribute.objects.filter(product=obj)
        return ProductAttributeSerializer(product_attrs, many=True).data