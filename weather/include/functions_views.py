"""Functions Views"""
from datetime import date, timedelta
from django.utils import timezone
from weather.models import Temperature
from .weather_parser import WeatherParser
from .temperature_color import temperature_color


def temperature_data(url, longitude_and_lattitude=None):
    '''Function returns dict with weather data prepared to pass to template.\n
    Data scraped and parsed using weatherParser.'''

    # cache time in minutes
    cache_time = 10

    parse_date = False
    temperature = None

    try:
        # temperature = Temperature.objects.get(
        #     geographical_coordinates=longitude_and_lattitude)
        # .latest()
        temperature = Temperature.objects.filter(
            geographical_coordinates=longitude_and_lattitude).latest('-last_downloaded')

        downloaded_date = temperature.last_downloaded
        date_now = timezone.now()

        if downloaded_date + timedelta(minutes=cache_time) < date_now:
            parse_date = True

    except Temperature.DoesNotExist:
        parse_date = True

    if parse_date:

        weather_parser = WeatherParser()
        weather_parser.set_url(url)
        weather_parser.set_weather_data()

        location = weather_parser.get_weather_location()

        current_temperature = weather_parser.get_current_temperature()

        if location is not None:
            temperature, created = Temperature.objects.update_or_create(
                geographical_coordinates=longitude_and_lattitude,
                defaults={
                    'location': location,
                    'temperature': current_temperature,
                    'icon': weather_parser.get_current_weather_icon()
                }
            )

    degree_sign = u"\N{DEGREE SIGN}"

    if temperature is not None:
        context = {
            'location': temperature.location,
            'longitude_and_lattitude': temperature.geographical_coordinates,
            'current_temp': f"{temperature.temperature}{degree_sign}",
            'temperature_color': temperature_color(temperature.temperature),
            'current_icon': temperature.icon,
            'current_date': date.today().strftime("%Y-%m-%d"),
        }
    else:
        context = {
            'longitude_and_lattitude': longitude_and_lattitude}

    return context
