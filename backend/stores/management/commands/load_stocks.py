from backend.stores.models import Store, StoreStock
from backend.products.models import Product
from backend.management.base import CustomBaseCommand
import pandas as pd


class Command(CustomBaseCommand):
    default_file_name = 'stocks.xlsx'

    def handle(self, *args, **options):
        StoreStock.objects.all().delete()

        file_name = options.get('file_name')
        abs_file_path = self.get_path_by_name(file_name, __file__)
        df = pd.read_excel(abs_file_path)

        #  index products in df
        products = Product.objects.filter(name__in=df['product'])
        indexed_products = {product.name: product for product in products}

        #  index stores in df
        store_names = list(df)[1:]
        stores = Store.objects.filter(name__in=store_names)
        indexed_stores = {store.name: store for store in stores}

        stocks = []
        for i, row in df.iterrows():
            for name in store_names:
                stocks.append(StoreStock(
                    count=row[name],
                    product=indexed_products[row['product']],
                    store=indexed_stores[name]
                    ))
        StoreStock.objects.bulk_create(stocks)

        print('----stores load done----')
