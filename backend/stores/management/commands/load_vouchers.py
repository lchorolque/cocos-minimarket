from backend.stores.models import Store, Voucher, ValidWeekday
from backend.products.models import Product
from backend.management.base import CustomBaseCommand
from backend.date_utils import WEEKDAYS
import pandas as pd
import json


class Command(CustomBaseCommand):
    default_file_name = 'vouchers.xlsx'

    def handle(self, *args, **options):
        Voucher.objects.all().delete()
        ValidWeekday.objects.all().delete()

        file_name = options.get('file_name')
        abs_file_path = self.get_path_by_name(file_name, __file__)
        df = pd.read_excel(abs_file_path)
        df = df.where(pd.notnull(df), None)

        #  index products in df
        products = Product.objects.all()
        indexed_products = {product.name: product for product in products}

        #  index stores in df
        store_names = set(df['store'])
        stores = Store.objects.filter(name__in=store_names)
        indexed_stores = {store.name: store for store in stores}

        # create ValidWeekdays
        indexed_weekdays = {}
        for day in WEEKDAYS:
            indexed_weekdays[day[0]] = ValidWeekday.objects.create(weekday=day[0])

        for i, row in df.iterrows():
            product_names = json.loads(row['products'])
            valid_days = json.loads(row['valid_days']) if row['valid_days'] else []

            #  init voucher with its plain data
            voucher = Voucher()
            for col, value in row[:'discount'].iteritems():
                setattr(voucher, col, value)

            voucher.store = indexed_stores[row['store']]
            voucher.save()

            #  set M2Ms
            voucher.products.set(
                [item[1] for item in indexed_products.items() if item[0] in product_names]
            )
            voucher.valid_weekdays.set(
                [item[1] for item in indexed_weekdays.items() if item[0] in valid_days]
            )

        print('----vouchers load done----')
