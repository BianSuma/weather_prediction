from django.forms import ModelForm, Textarea
from django.db import models
import datetime

# Create your models here.


class Weathers(models.Model):
    tanggal = models.DateField()
    temp_maks = models.FloatField(max_length=5)
    temp_min = models.FloatField(max_length=5)
    temp_med = models.FloatField(max_length=5)
    hum_rel = models.FloatField(max_length=5)
    wind_speed = models.FloatField(max_length=5)
    weather_summary = models.TextField(max_length=56)


class Meta:
    db_table = 'weather_predict'
