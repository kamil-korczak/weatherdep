"""Functions Views"""
from datetime import date, timedelta
from django.utils import timezone
from weather.models import Temperature
from .weather_parser import weatherParser
from .temperature_color import temperature_color


def temperature_data(url, longitude_and_lattitude=None):
    '''Function returns dict with weather data prepared to pass to template.\n 
    Data scraped and parsed using weatherParser.'''

    # cache time in minutes
    cache_time = 15

    parse_date = False

    try:
        temperature = Temperature.objects.get(geographical_coordinates=longitude_and_lattitude)

        downloaded_date = temperature.last_downloaded
        date_now = timezone.now()

        if downloaded_date + timedelta(minutes=cache_time) < date_now:
            parse_date = True

    except Temperature.DoesNotExist:
        parse_date = True

    if parse_date:

        weather_parser = weatherParser()
        weather_parser.setUrl(url)
        weather_parser.setWeatherData()    

        location = weather_parser.getWeatherLocation()

        current_temperature = weather_parser.getCurrentTemperature()

        temperature, created = Temperature.objects.update_or_create( \
            geographical_coordinates=longitude_and_lattitude,
            defaults = {
                'location': location,
                'current_temp': current_temperature,
                'temperature_color': temperature_color(current_temperature),
                'current_icon': weather_parser.getCurrentWeatherIcon()
            }
        )

    context = {
            'location': temperature.location,
            'longitude_and_lattitude': temperature.geographical_coordinates,
            'current_temp': temperature.current_temp,
            'temperature_color': temperature.temperature_color,
            'current_icon': temperature.current_icon,
            'current_date': date.today().strftime("%Y-%m-%d"),
        }

    return context
