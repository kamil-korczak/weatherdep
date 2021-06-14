"""Functions Views"""
from datetime import date, datetime, timedelta

import pytz
from django.db.models import Avg
from weather.include.weather_parser import coordinates_str
from weather.models import (City, Country, County, PickedCity, Temperature,
                            Voivodeship)

from ..temperature_color import temperature_color

DEGREE_SIGN = u"\N{DEGREE SIGN}"


def get_temperature_context_data_by_url(url: str, past_week: int = 0) -> dict:
    '''Function returns dict with weather data prepared to pass to template.\n
    Data scraped and parsed using weatherParser.'''
    longitude_and_lattitude = coordinates_str(url)

    temperature, parse_data = Temperature.objects.get_object_by_coordinates_or_parse(
        coordinates=longitude_and_lattitude)

    if parse_data:
        temperature = Temperature.objects.create(
            Temperature.objects.get_weather_data(url))

    return prepare_context_temperature_data(temperature, longitude_and_lattitude, past_week)


def prepare_context_temperature_data(temperature,
                                     longitude_and_lattitude: str,
                                     past_week: int) -> dict:
    '''Function returns dict with weather data prepared to pass to template'''

    if temperature:
        context = {
            'city': temperature.city,
            'longitude_and_lattitude': temperature.city.geographical_coordinates,
            'current_temp': f"{temperature.temperature}{DEGREE_SIGN}",
            'temperature_color': temperature_color(temperature.temperature),
            'current_icon': temperature.icon,
            'current_date': date.today().strftime("%Y-%m-%d"),
        }

        try:
            if temperature.city.picked_city_related:
                date_start, date_end = get_date_range_by_past_week(past_week)
                date_range = get_date_range_str_from_dates(
                    date_start, date_end)

                temperatures = Temperature.objects.get_of_picked_city_with_date_range(
                    date_start, date_end, city_id=temperature.city_id)  # .aggregate(

                temperatures = Temperature.objects.filter(
                    id__in=[temperature['id'] for temperature in temperatures]
                ).aggregate(temperature_avg=Avg('temperature'))

                if temperatures:
                    context['temperature_avg'] = temperatures['temperature_avg']

                context['date_range'] = date_range
        except PickedCity.DoesNotExist:
            pass

    else:
        context = {
            'longitude_and_lattitude': longitude_and_lattitude}

    return context


def get_country_context(country, past_week):
    date_start, date_end = get_date_range_by_past_week(past_week)
    date_range = get_date_range_str_from_dates(date_start, date_end)

    temperatures = Temperature.objects.get_of_picked_city_with_date_range(
        date_start, date_end)

    country = Country.objects.get_with_average_temperature(
        temperatures)

    voivodeships = Voivodeship.objects.get_all_with_average_temperature(
        temperatures)

    return prepare_country_context(country, voivodeships, date_range)


def prepare_country_context(country, voivodeships, date_range):
    if country:
        return {
            'country': country,
            'voivodeships': voivodeships,
            'date_range': date_range,
        }
    return None


def get_voivodeship_context(country, voivodeship, past_week):
    date_start, date_end = get_date_range_by_past_week(past_week)
    date_range = get_date_range_str_from_dates(date_start, date_end)

    country = Country.objects.filter(name__iexact=country).last()

    voivodeship_obj = Voivodeship.objects.filter(
        name__iexact=voivodeship).last()

    if voivodeship_obj:
        temperatures = Temperature.objects.get_of_picked_city_with_date_range(
            date_start, date_end)

        voivodeship = Voivodeship.objects.get_with_average_temperature(
            voivodeship_obj.id, temperatures)

        counties = County.objects.get_all_with_average_temperature(
            voivodeship_obj.id, temperatures)
    else:
        counties = None

    return prepare_voivodeship_context(country, voivodeship, counties, date_range)


def prepare_voivodeship_context(country, voivodeship, counties, date_range):
    if country and voivodeship and counties:
        return {
            'country': country,
            'voivodeship': voivodeship,
            'counties': counties,
            'date_range': date_range,
        }

    if isinstance(voivodeship, str):
        return {'voivodeship_str': voivodeship}

    return {'voivodeship': voivodeship}


def get_county_context(country, voivodeship, county, past_week):
    date_start, date_end = get_date_range_by_past_week(past_week)
    date_range = get_date_range_str_from_dates(date_start, date_end)

    voivodeship_obj = Voivodeship.objects.filter(
        name__iexact=voivodeship).last()

    if voivodeship_obj:
        voivodeship = voivodeship_obj

        county_obj = County.objects.filter(name__iexact=county).last()

        if county_obj:

            temperatures = Temperature.objects.get_of_picked_city_with_date_range(
                date_start, date_end)

            county = County.objects.get_with_average_temperature(
                county_obj.id, temperatures)

            cities = City.objects.get_all_with_average_temperature(
                county_obj.pk, temperatures
            )
    else:
        cities = None

    return prepare_county_context(country, voivodeship, county, cities, date_range)


def prepare_county_context(country, voivodeship, county, cities, date_range):
    if country and voivodeship and county and cities:
        return {
            'country': country,
            'voivodeship': voivodeship,
            'county': county,
            'cities': cities,
            'date_range': date_range,
        }

    if isinstance(voivodeship, str):
        return {'voivodeship_str': voivodeship}

    if isinstance(county, str):
        return {'county_str': county}

    return {'voivodeship': voivodeship, 'county': county}


def get_past_week(request):
    return int(request.GET.get('week-ago', 0))


def get_date_range_by_past_week(past_week):
    days = past_week * 7

    now = datetime.now(pytz.timezone('Europe/Warsaw'))
    today_start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end_day = now.replace(hour=23, minute=59, second=59, microsecond=0)

    date_start = today_start_day - timedelta(days + 6)
    date_end = today_end_day - timedelta(days)

    return [date_start, date_end]


def get_date_range_str_from_dates(date_start, date_end):
    return f'{date_start.strftime("%Y-%m-%d")} - {date_end.strftime("%Y-%m-%d")}'
