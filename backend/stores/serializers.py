from rest_framework import serializers
from backend.stores.models import Store, StoreStock, Cart, Voucher, CartStock
from backend.products.serializers import ProductSerializer
from django.db.models import F, Sum, FloatField

class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = '__all__'


class StoreStockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    store_name = serializers.CharField(source='store.name')

    class Meta:
        model = StoreStock
        fields = ('id', 'store', 'store_name', 'product')


class UpdateCartSerializer(serializers.Serializer):
    voucher_code = serializers.CharField(required=False, allow_null=True,
                                         allow_blank=True, write_only=True)
    product = serializers.IntegerField(required=False, write_only=True)
    add_product = serializers.BooleanField(default=True, write_only=True)

    def validate_voucher_code(self, value):
        """
        Check if voucher code exist
        """
        if value and not Voucher.objects.filter(code=value):
            raise serializers.ValidationError("Incorrect code of voucher")

    def validate(self, data):
        """
        Check if store have stock
        """
        store = self.instance.store
        if data['product'] and data['add_product']:
            if not store.store_stocks.filter(count__gt=0, product_id=data['product']):
                raise serializers.ValidationError("non stock for this product")
        return data

    def update(self, instance, validated_data):
        voucher_code = validated_data['voucher_code']
        product_id = validated_data['product']

        if voucher_code:
            instance.voucher = Voucher.objects.get(code=voucher_code)
            instance.save()
        if product_id:
            stock = CartStock.objects.get_or_create(cart=instance, product_id=product_id)[0]
            if validated_data['add_product']:
                stock.count += 1
            elif stock.count > 0:   # check if have stock to subtract
                stock.count -= 1
            stock.save()
        return instance


class CartSerializer(serializers.Serializer):
    total_products = serializers.SerializerMethodField(read_only=True)
    total_discounted_products = serializers.SerializerMethodField(read_only=True)

    def get_total_products(self, instance, apply_vaucher=False):
        cart_stocks = instance.cart_stocks.all()

        products = cart_stocks\
            .annotate(total=Sum(F('product__price') * F('count'), output_field=FloatField()))\
            .values('product_id', 'product__name', 'count', 'product__price', 'total')

        if apply_vaucher:
            voucher = instance.voucher
            if voucher:  # apply voucher discounts
                indexed_products = {product['product_id']: product for product in products}
                product_discounts = voucher.product_discounts(cart_stocks)  # get discounts dict
                for product_id, discount in product_discounts.items():  # apply discount
                    indexed_products[product_id]['total'] -= discount

        return {
            'products': products,
            'total': sum(product['total'] for product in products)
        }

    def get_total_discounted_products(self, instance):
        return self.get_total_products(instance, apply_vaucher=True)
