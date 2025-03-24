from django.db import models
from users.models import User
from products.models import Product
# Create your models here.


class Cart():
    cart_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
cart_item = models.ForeignKey(User, on_delete=models.CASCADE)



class Cart_item():
     cart_item_id = models.AutoField(primary_key=True)
     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
     quantity = models.IntegerField()
     price = models.FloatField()
     subtotal = models.FloatField()



