from django.db import models

# Create your models here.



# Create your models here.
class Attribute(models.Model):
 attribute_ID = models.AutoField(primary_key=True)
 name = models.CharField(max_length=200)

