from backend.products.models import Product, Category
from backend.management.base import CustomBaseCommand
import pandas as pd


class Command(CustomBaseCommand):
    default_file_name = 'products_n_categories.xlsx'

    def handle(self, *args, **options):
        """
        if we want to perform the load, we need to use "bulk_create" and we
        need to model the intermediary of the M2Ms between Category and Product
        """
        Product.objects.all().delete()
        Category.objects.all().delete()

        file_name = options.get('file_name')
        abs_file_path = self.get_path_by_name(file_name, __file__)
        df = pd.read_excel(abs_file_path)

        indexed_categories = {}
        for i, row in df.iterrows():
            category = indexed_categories.get(row['category'])
            if not category:
                category = Category.objects.create(name=row['category'])
                indexed_categories[category.name] = category

            #  if the product is in more than one row, we keep price of the last one
            product = Product.objects.update_or_create(name=row['product'],
                                                       defaults={'price': row['price']})[0]
            product.categories.add(category)

        print('----products and categories load done----')
