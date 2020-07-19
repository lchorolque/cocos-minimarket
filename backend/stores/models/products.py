from django.db import models
from backend.date_utils import WEEKDAYS


class Stock(models.Model):
    count = models.IntegerField(default=0)

    class Meta:
        abstract = True


class StoreStock(Stock):
    product = models.ForeignKey('products.Product', related_name='store_stocks', on_delete=models.CASCADE)
    store = models.ForeignKey('Store', related_name='store_stocks', on_delete=models.CASCADE)


class CartStock(Stock):
    product = models.ForeignKey('products.Product', related_name='cart_stocks', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', related_name='cart_stocks', on_delete=models.CASCADE)


class Voucher(models.Model):
    code = models.CharField(max_length=25, unique=True)  # TODO implement hash to auto generate
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    min_units = models.IntegerField(default=0)
    max_units = models.IntegerField(null=True)
    discount = models.FloatField()
    store = models.ForeignKey('Store', related_name='vouchers', on_delete=models.CASCADE)
    products = models.ManyToManyField('products.Product', related_name='vouchers')



class ValidWeekday(models.Model):
    weekday = models.IntegerField(default=0, choices=WEEKDAYS)
    vouchers = models.ManyToManyField('Voucher', related_name='valid_weekdays')


class Cart(models.Model):
    owner = models.ForeignKey('auth.User', related_name='carts', on_delete=models.CASCADE)
