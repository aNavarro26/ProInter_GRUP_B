from django.db import models
from users.models import User
from products.models import Product

# Create your models here.


class Order:
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()
    status = models.CharField(max_length=100)


class Order_item:
    order_item_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class Shipment:
    shipment_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    shipment_date = models.DateField()
