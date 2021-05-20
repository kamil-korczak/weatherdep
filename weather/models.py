from datetime import timedelta
from typing import Any, Tuple

from django.db import models
from django.utils import timezone

from .include.models.random_locations_data import RandomLocationsData
from .include.weather_parser import WeatherParser, coordinates_str

# cache time in minutes
CACHE_TIME = 15


class TemperatureManager(models.Manager):

    def generate_random_locations(self):
        pass
        # RandomLocationsData(count=10)

    def get_object_by_coordinates_or_parse(self, coordinates: str) -> Tuple[Any, bool]:
        parse_data = False
        temperature = None

        try:
            temperature = self.filter(
                geographical_coordinates=coordinates).latest('-last_downloaded')

            # print(temperature.query)

            downloaded_date = temperature.last_downloaded
            date_now = timezone.now()

            if downloaded_date + timedelta(minutes=CACHE_TIME) < date_now:
                parse_data = True

        except Temperature.DoesNotExist:
            parse_data = True

        return [temperature, parse_data]

    def update_or_create_object(self, url: str) -> Tuple[Any, bool]:
        weather_parser = WeatherParser(url)

        location = weather_parser.get_weather_location()
        current_temperature = weather_parser.get_current_temperature()

        if location is not None:

            longitude_and_lattitude = coordinates_str(
                weather_parser.get_weather_url())

            return self.update_or_create(
                geographical_coordinates=longitude_and_lattitude,
                defaults={
                    'location': location,
                    'temperature': current_temperature,
                    'icon': weather_parser.get_current_weather_icon()
                }
            )

        return [None, False]


class Temperature(models.Model):
    location = models.CharField(max_length=200)
    geographical_coordinates = models.CharField(max_length=200, null=True)
    temperature = models.IntegerField()
    icon = models.CharField(max_length=8)
    last_downloaded = models.DateTimeField(
        'date downloaded', auto_now=True, blank=True)

    objects = TemperatureManager()
