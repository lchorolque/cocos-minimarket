import django_filters
from backend.stores.models import Store
from datetime import datetime


class StoreFilter(django_filters.FilterSet):
    is_open = django_filters.BooleanFilter(method="is_open_filter")

    def is_open_filter(self, queryset, name, value):
        if not value:
            return queryset
        datetime_today = datetime.today()

        queryset = queryset.filter(
            open_times__hours_ranges__start_hour__lte=datetime_today,
            open_times__hours_ranges__end_hour__gte=datetime_today,
            open_times__weekday=datetime_today.weekday()
            ).distinct()
        return queryset

    class Meta:
        model = Store
        fields = ['is_open']
