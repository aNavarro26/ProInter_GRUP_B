from django.db import models
from ProInter_GRUP_B.axion import users
from ProInter_GRUP_B.axion import products
# Create your models here.


class Cart():
    cart_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(users, on_delete=models.CASCADE)
cart_item = models.ForeignKey(users, on_delete=models.CASCADE)



class Cart_item():
     cart_item_id = models.AutoField(primary_key=True)
     product_id = models.ForeignKey(products, on_delete=models.CASCADE)
     quantity = models.IntegerField()
     price = models.FloatField()
     subtotal = models.FloatField()



