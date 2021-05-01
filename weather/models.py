from django.db import models


class Temperature(models.Model):
    location = models.CharField(max_length=200)
    geographical_coordinates = models.CharField(max_length=200, null=True)
    temperature = models.IntegerField()
    icon = models.CharField(max_length=8)
    last_downloaded = models.DateTimeField(
        'date downloaded', auto_now=True, blank=True)
