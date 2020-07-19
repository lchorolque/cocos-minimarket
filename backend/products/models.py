from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()


class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField('Product', related_name='categories')
