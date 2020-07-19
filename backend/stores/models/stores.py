from django.db import models
from backend.date_utils import WEEKDAYS


class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='stores')


class OpenTime(models.Model):
    weekday = models.IntegerField(default=0, choices=WEEKDAYS)
    store = models.ForeignKey('Store', related_name='open_times', on_delete=models.CASCADE)


class HoursRange(models.Model):
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    open_times = models.ManyToManyField('OpenTime', related_name='hours_ranges')
