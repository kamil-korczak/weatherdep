"""Functions Views"""
from datetime import date

from weather.models import Temperature
from weather.include.weather_parser import coordinates_str

from ..temperature_color import temperature_color

DEGREE_SIGN = u"\N{DEGREE SIGN}"


def get_temperature_context_data_by_url(url: str) -> dict:
    '''Function returns dict with weather data prepared to pass to template.\n
    Data scraped and parsed using weatherParser.'''

    parse_data = False
    temperature = None

    longitude_and_lattitude = coordinates_str(url)

    temperature, parse_data = Temperature.objects.get_object_by_coordinates_or_parse(
        coordinates=longitude_and_lattitude)

    if parse_data:
        temperature, created = Temperature.objects.update_or_create_object(
            Temperature.objects.get_weather_data(url))

    return prepare_context_temperature_data(temperature, longitude_and_lattitude)


def prepare_context_temperature_data(temperature_obj, longitude_and_lattitude: str) -> dict:
    '''Function returns dict with weather data prepared to pass to template'''

    if temperature_obj is not None:

        context = {
            'location': temperature_obj.location,
            'longitude_and_lattitude': temperature_obj.geographical_coordinates,
            'current_temp': f"{temperature_obj.temperature}{DEGREE_SIGN}",
            'temperature_color': temperature_color(temperature_obj.temperature),
            'current_icon': temperature_obj.icon,
            'current_date': date.today().strftime("%Y-%m-%d"),
        }
    else:
        context = {
            'longitude_and_lattitude': longitude_and_lattitude}

    return context
