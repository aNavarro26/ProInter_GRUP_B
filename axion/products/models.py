from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class Product(models.Model):
    SERIES_CHOICES = [
        ("Flagship", "Flagship"),
        ("Mid-range", "Mid-range"),
        ("Budget", "Budget"),
    ]

    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True)
    price = models.FloatField()
    stock = models.IntegerField()
    series = models.CharField(max_length=20, choices=SERIES_CHOICES)


class Attribute(models.Model):
    attribute_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class ProductAttribute(models.Model):
    product_attribute_id = models.AutoField(primary_key=True)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    attribute = models.ForeignKey("products.Attribute", on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
