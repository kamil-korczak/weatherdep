from .weather_parser import weatherParser
from .temperature_color import temperature_color

from datetime import date

def temperature_data(url, longitude_and_lattitude=None):
    '''Function returns dict with weather data prepared to pass to template.\n 
    Data scraped and parsed using weatherParser.'''

    wp = weatherParser()
    wp.setUrl(url)
    wp.setWeatherData()

    today = date.today()

    location = wp.getWeatherLocation()

    current_temperature = wp.getCurrentTemperature()

    context = {
        'location': location,
        'longitude_and_lattitude': longitude_and_lattitude,
        'current_temp': current_temperature,
        'temperature_color': temperature_color(current_temperature),
        'current_icon': wp.getCurrentWeatherIcon(),
        'current_date': today.strftime("%Y-%m-%d"),
    }

    return context