# Generated by Django 5.1.7 on 2025-04-20 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_image_url_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=800),
        ),
    ]
