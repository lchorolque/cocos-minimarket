from backend.stores.models import Store, OpenTime, HoursRange
from backend.management.base import CustomBaseCommand
import pandas as pd
import json


class Command(CustomBaseCommand):
    default_file_name = 'stores.xlsx'

    def handle(self, *args, **options):
        Store.objects.all().delete()

        file_name = options.get('file_name')
        abs_file_path = self.get_path_by_name(file_name, __file__)
        df = pd.read_excel(abs_file_path)

        for i, row in df.iterrows():
            logo_path = self.get_path_by_name(row['logo'], __file__)
            store = Store(
                name=row['name'],
                address=row['address'],
                logo=logo_path,
            )
            store.save()

            #   create open times for the store
            open_times = json.loads(row['open_time'])
            for open_time in open_times:
                #  create hours ranges
                hour_ranges_list = open_time['hours']
                hours_ranges = []
                for h_range in hour_ranges_list:
                    hours_ranges.append(
                        HoursRange.objects.create(start_hour=h_range[0], end_hour=h_range[1])
                    )
                #  create open time objects and set its hours ranges
                days = open_time['days']
                for day in days:
                    open_time = OpenTime.objects.create(weekday=day, store=store)
                    open_time.hours_ranges.set(hours_ranges)

        print('----stores load done----')
