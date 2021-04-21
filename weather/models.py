from django.db import models

# Create your models here.

class Temperature(models.Model):
    location = models.CharField(max_length=200)
    geographical_coordinates = models.CharField(max_length=200, null=True)
    current_temp = models.CharField(max_length=5)
    temperature_color = models.CharField(max_length=3)
    current_icon = models.CharField(max_length=100)
    last_downloaded = models.DateTimeField('date downloaded', auto_now=True, blank=True)
