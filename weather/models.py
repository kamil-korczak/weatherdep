import math
import random
import re
import time
from datetime import timedelta
from typing import Any, Tuple

import pandas as pd
from django.db import models
from django.db.models import Avg
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.functions.datetime import TruncDay
from django.utils import timezone
from geopy.geocoders import Nominatim

from .include.models.random_locations_data import RandomLocationsData
from .include.weather_parser import WeatherParser, coordinates_str

# cache time in minutes
CACHE_TIME = 15


def timing(func):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = func(*args, **kwargs)
        time2 = time.time()

        time_elapsed = (time2-time1)
        count_minutes = math.floor(time_elapsed / 60.0)
        count_seconds = math.floor(time_elapsed - count_minutes * 60)
        count_miliseconds = round(
            (time_elapsed-count_minutes*60-count_seconds) % 1000.0 * 1000.0)

        print(f'### {func.__name__} function took \
        {count_minutes} m {count_seconds} s .{count_miliseconds} ms ###')

        return ret
    return wrap


class TemperatureManager(models.Manager):

    @staticmethod
    def generate_random_locations(count=5):
        RandomLocationsData(temperature_class=Temperature, count=count)

    def get_object_by_coordinates_or_parse(self, coordinates: str) -> Tuple[Any, bool]:
        parse_data = False
        temperature = None

        try:
            temperature = self.filter(
                city__geographical_coordinates=coordinates).latest('downloaded')

            downloaded_date = temperature.downloaded
            date_now = timezone.now()

            if downloaded_date + timedelta(minutes=CACHE_TIME) < date_now:
                parse_data = True

        except Temperature.DoesNotExist:
            parse_data = True

        return [temperature, parse_data]

    @staticmethod
    def get_weather_data(url: str) -> dict:
        weather_parser = WeatherParser(url)

        weather_data = {
            'location': weather_parser.get_weather_location(),
            'geographical_coordinates': coordinates_str(
                weather_parser.get_weather_url()),
            'temperature': weather_parser.get_current_temperature(),
            'icon': weather_parser.get_current_weather_icon()
        }
        return weather_data

    def create(self, weather_data: dict, city=None) -> bool:
        if not city:
            city = City.objects.get_city(
                coordinates=weather_data['geographical_coordinates'])

        if weather_data['location'] and city:
            return super().create(
                temperature=weather_data['temperature'],
                city=city,
                icon=weather_data['icon'],
            )

        return None

    @timing
    def get_for_picked_cities(self):
        cities = PickedCity.objects.all()
        city_count = cities.count()
        print(f"### started process {city_count} cities. ###")
        i_counter = 0
        for picked_city in cities:
            i_counter += 1
            if i_counter % 10 == 0:
                print(
                    f"# Processing [{i_counter}/{city_count}][#{picked_city.city_id}] cities.")
            self.get_by_location_of_picked_city(picked_city=picked_city.city)

    def get_by_location_of_picked_city(self, picked_city):
        name = picked_city.name
        voivodeship = picked_city.county.voivodeship.name
        if "(" in name:
            name = re.sub(r'\ \(.*\)', '', name)

        weather_data = Temperature.objects.get_weather_data(
            url=f"{name} {voivodeship}")

        City.objects.check_and_update_coordinates(
            obj=picked_city,
            coordinates=weather_data['geographical_coordinates'])

        self.create(weather_data=weather_data, city=picked_city)

    def get_of_picked_city_with_date_range(self, date_start, date_end, city_id=None):
        temperature_kwargs = {
            'downloaded__range': [f'{date_start}', f'{date_end}']
        }

        if not city_id:
            temperature_kwargs['city__picked_city_related__isnull'] = False
        else:
            temperature_kwargs['city__exact'] = city_id

        query_set = self.filter(
            **temperature_kwargs
        ).values('id', 'city__name').annotate(
            day=TruncDay('downloaded')
        ).order_by('day', 'city__name', '-temperature'
                   ).distinct('day', 'city__name')

        return query_set


class PickedCityManager(models.Manager):

    def set_random_cities(self, count=5):
        counties = County.objects.all()

        picked_already = list(PickedCity.objects.all())

        for county in counties:
            picked_cities_counter = PickedCity.objects.filter(
                city__county__exact=county.id).count()

            max_counter = count

            if picked_cities_counter < max_counter:

                cities_count = City.objects.filter(
                    county__exact=county.id).count()

                if max_counter > cities_count:
                    max_counter = cities_count

                while picked_cities_counter < max_counter:
                    cities = City.objects.filter(
                        country__name__iexact="Polska",
                        county__exact=county
                    )

                    city = random.choice(cities)

                    picked_obj = PickedCity(city.id)

                    if picked_obj not in picked_already:
                        picked_cities_counter += 1

                        print(f'[Set as picked] city_name: | {city.name} | \
                            {city.county.voivodeship.name} | {city.county.name} | [{city.id}]')

                        picked_already.append(picked_obj)

                        self.create(city=city)


class CityManager(models.Manager):
    def load_data_from_csv(self, debug=False):
        data = pd.read_csv("spis_kody.csv", header=None, delimiter=';',
                           names=['postcode', 'city', 'null1', 'null2',
                                  'commune', 'county', 'voivodeship'])
        data = pd.DataFrame(data)

        data = data.drop_duplicates(subset=['county', 'city'])

        debug_iter = 0

        for index, row in data.iterrows():

            country = Country.objects.filter(name="Polska").last()

            if not country:
                country = Country(name="Polska")
                country.save()

            voivodeship = Voivodeship.objects.filter(
                name=row.voivodeship).last()

            if not voivodeship:
                voivodeship = Voivodeship(name=row.voivodeship)
                voivodeship.save()

            county = County.objects.filter(
                name=row.county, voivodeship=voivodeship).last()

            if not county:
                county = County(name=row.county, voivodeship=voivodeship)
                county.save()

            city = City.objects.filter(name=row.city, county=county).last()

            if not city:
                if debug:
                    print(f"Creating[{index}] {row.city}")
                self.create(
                    name=row.city,
                    county=county,
                    country=country
                )
            else:
                if debug:
                    print(f"[{index}] {row.city} was already added.")

            if not debug:
                debug_iter += 1

                if debug_iter % 500 == 0:
                    print(f"Indexed [{debug_iter}]")

    def get_city_name_from_address(self, address):
        return address.get('city',
                           address.get('town',
                                       address.get('village', '')))

    def get_city(self, coordinates):
        city = City.objects.filter(
            geographical_coordinates__exact=coordinates).last()

        if not city:
            print("TRYING TO GET CITY NAME USING GEOPY")
            geolocator = Nominatim(user_agent="Weather APP")
            location = geolocator.reverse(coordinates, language='pl')

            print(f'location: {location}')

            city = None

            if location:
                print(f'raw: {location.raw}')

                address_raw = location.raw['address']

                country_code = address_raw.get('country_code')

                if country_code:

                    if country_code == 'pl':
                        city = self._get_polish_city(address=address_raw)
                    else:
                        city = self._get_or_create_international_city(
                            address=address_raw)

                    if city:
                        self.check_and_update_coordinates(
                            obj=city, coordinates=coordinates)

        return city

    def _get_polish_city(self, address):
        state_name = address['state'].replace(
            'województwo ', '')

        city_name = self.get_city_name_from_address(address)

        city = City.objects.filter(
            name__icontains=city_name, county__voivodeship__name__iexact=state_name) \
            .order_by('name').first()

        return city

    @classmethod
    def check_and_update_coordinates(cls, obj, coordinates):
        if coordinates and not obj.geographical_coordinates:
            obj.geographical_coordinates = coordinates
            obj.save()

    def _get_or_create_international_city(self, address):
        print(f'address: {address}')

        city_name = self.get_city_name_from_address(address)

        if city_name:
            country, country_created = Country.objects.get_or_create(
                name=address['country'])
            city, city_created = self.get_or_create(
                name=city_name, country=country)
            return city

        return None

    def get_all_with_average_temperature(self, county_id, temperatures):
        temperature_lookup = 'temperature_related__'
        cities_kwargs = {
            'county__exact': county_id,
            f'{temperature_lookup}in': [temperature['id'] for temperature in temperatures]
        }

        query_set = self.filter(
            **cities_kwargs
        ).values('name', 'geographical_coordinates').annotate(
            temperature_avg=Avg(''.join([temperature_lookup, 'temperature']))
        ).order_by('picked_city_related',
                   'geographical_coordinates', 'name')

        return query_set


class CountryManager(models.Manager):
    def get_with_average_temperature(self, temperatures):
        temperature_lookup = 'city_related_to_country__temperature_related__'
        country_kwargs = {
            f'{temperature_lookup}in': [temperature['id'] for temperature in temperatures]
        }

        return self.filter(**country_kwargs).annotate(
            temperature_avg=(Avg(''.join([temperature_lookup, 'temperature'])))
        ).last()


class VoivodeshipManager(models.Manager):
    def get_all_with_average_temperature(self, temperatures):
        return self.get_with_average_temperature(
            voivodeship_id=None, temperatures=temperatures)

    def get_with_average_temperature(self, voivodeship_id, temperatures):
        temperature_lookup = 'county_related__city_related_to_county__temperature_related__'

        voivodeships_kwargs = {
            f'{temperature_lookup}in': [temperature['id'] for temperature in temperatures]
        }

        if voivodeship_id:
            voivodeships_kwargs['id'] = voivodeship_id

        query_set = self.filter(
            **voivodeships_kwargs
        ).values('name').annotate(
            temperature_avg=Avg(''.join([temperature_lookup, 'temperature']))
        ).order_by('name')

        return query_set if not voivodeship_id else query_set.last()


class CountyManager(models.Manager):
    def get_all_with_average_temperature(self, voivodeship_id, temperatures):
        return self.get_with_average_temperature(
            county_id=None, temperatures=temperatures, voivodeship_id=voivodeship_id)

    def get_with_average_temperature(self, county_id, temperatures, voivodeship_id=None):
        temperature_lookup = 'city_related_to_county__temperature_related__'

        counties_kwargs = {
            f'{temperature_lookup}in': [temperature['id'] for temperature in temperatures]
        }

        if not county_id:
            counties_kwargs['voivodeship_id'] = voivodeship_id
        else:
            counties_kwargs['id'] = county_id

        query_set = self.filter(
            **counties_kwargs
        ).values('name').annotate(
            temperature_avg=Avg(''.join([temperature_lookup, 'temperature']))
        ).order_by('name')

        return query_set if not county_id else query_set.last()


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    objects = CountryManager()


class Voivodeship(models.Model):
    name = models.CharField(max_length=50, unique=True)

    objects = VoivodeshipManager()


class County(models.Model):
    voivodeship = models.ForeignKey(
        Voivodeship, related_name="county_related", on_delete=PROTECT)
    name = models.CharField(max_length=50)

    objects = CountyManager()

    class Meta:
        unique_together = ['name', 'voivodeship']


class City(models.Model):
    country = models.ForeignKey(
        Country, related_name="city_related_to_country", on_delete=PROTECT)
    county = models.ForeignKey(
        County, related_name="city_related_to_county", on_delete=PROTECT, null=True)
    name = models.CharField(max_length=50)
    geographical_coordinates = models.CharField(max_length=200, null=True)

    objects = CityManager()


class PickedCity(models.Model):
    city = models.OneToOneField(
        City,
        related_name="picked_city_related",
        on_delete=models.CASCADE,
        primary_key=True
    )

    objects = PickedCityManager()


class Temperature(models.Model):
    city = models.ForeignKey(
        City, related_name="temperature_related", on_delete=CASCADE)

    temperature = models.IntegerField()
    icon = models.CharField(max_length=8)
    downloaded = models.DateTimeField(
        'date downloaded', auto_now=True, blank=True)

    objects = TemperatureManager()
