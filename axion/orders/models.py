from django.db import models
from ProInter_GRUP_B.axion import users
from ProInter_GRUP_B.axion import products
# Create your models here.

class Order():
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(users, on_delete=models.CASCADE)
    order_date = models.DateField()
    status = models.CharField(max_length=100)


class Order_item():
    order_item_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(products, on_delete=models.CASCADE)