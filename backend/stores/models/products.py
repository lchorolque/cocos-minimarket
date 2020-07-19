from django.db import models
from backend.date_utils import WEEKDAYS
from datetime import datetime


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

    def product_discounts(self, stocks):
        def is_valid_today():
            today = datetime.today().date()
            if self.start_date <= today and self.end_date >= today:
                valid_weekdays = self.valid_weekdays.all().values_list('weekday', flat=True)
                if not valid_weekdays or today.weekday() in valid_weekdays:   # not days is all days
                    return True
            return False

        def discount_amounts(stock):
            price = stock.product.price
            count = stock.count
            max_units = self.max_units

            if max_units:   # set count like max_units
                count = count if count < max_units else max_units

            discountable_units = count // self.min_units
            discountable_amount = price * self.discount
            discount_amount = discountable_amount * discountable_units

            return discount_amount

        discounts = {}
        if is_valid_today():
            #  filter availables stocks
            available_stocks = stocks.filter(product__in=self.products.all())

            for stock in available_stocks:
                discount_amount = discount_amounts(stock)
                discounts[stock.product.id] = discount_amount

        return discounts


class ValidWeekday(models.Model):
    weekday = models.IntegerField(default=0, choices=WEEKDAYS)
    vouchers = models.ManyToManyField('Voucher', related_name='valid_weekdays')


class Cart(models.Model):
    owner = models.ForeignKey('auth.User', related_name='carts', on_delete=models.CASCADE)
    store = models.ForeignKey('Store', related_name='carts', on_delete=models.CASCADE)
    voucher = models.ForeignKey('Voucher', related_name='carts',
                                null=True, on_delete=models.SET_NULL)
