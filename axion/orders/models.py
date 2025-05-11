from django.db import models
from users.models import User
from products.models import Product
from datetime import date


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    subtotal = models.FloatField()


class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="shipments")
    shipment_date = models.DateField()


class Payment(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    method = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=7)
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"Payment for Order {self.order.order_id}"
