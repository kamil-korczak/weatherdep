# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import resolve
from .include.weather_parser import weatherParser
from .include.temperature_color import temperature_color
# Create your views here.

# test location  '52.044712511740244,15.621827286963514'
# test location - error '1000.99999999,20000.99999'

#http://192.168.1.3:9005/temperature/zielona_gora
#http://192.168.1.3:9005/temperature/current/32.044712511740244,15.621827286963514/

from datetime import date

def index(request):
    template = loader.get_template('weather/index.html')

    return HttpResponse(template.render(None, request))

def temperatureZG(request, longitude=False, lattitude=False):
    '''(Task Version) View responsible for displaying temperature of Zielona Góra.'''
    template = loader.get_template('weather/temperature.html')

    url = 'zielona-góra-zielona-góra-poland/51.93548,15.50643'

    wp = weatherParser()
    wp.setUrl(url)
    wp.setWeatherData()

    today = date.today()

    location = wp.getWeatherLocation()

    current_temperature = wp.getCurrentTemperature()

    context = {
        'location': location,
        'longitude_and_lattitude': None,
        'current_temp': current_temperature,
        'temperature_color': temperature_color(current_temperature),
        'current_icon': wp.getCurrentWeatherIcon(),
        'current_date': today.strftime("%Y-%m-%d"),
    }

    return HttpResponse(template.render(context, request))

def temperatureGC(request, longitude=False, lattitude=False):
    '''(Task Version) View responsible for displaying temperature based on geographical coordinates.'''
    template = loader.get_template('weather/temperature.html')

    url = f'{longitude},{lattitude}'
    longitude_and_lattitude = url.replace(',', ', ')

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

    return HttpResponse(template.render(context, request))

def temperature2(request, longitude=False, lattitude=False):
    '''(Version 2) View of combined views responsible for displaying temperature:
    * of Zielona Góra
    * and based on geographical coordinates.'''
    template = loader.get_template('weather/temperature.html')

    current_url = resolve(request.path_info).url_name

    if current_url == 'zielona-gora2':
        url = 'zielona-góra-zielona-góra-poland/51.93548,15.50643'
        longitude_and_lattitude = None

    elif current_url == 'other-location2':
        url = f'{longitude},{lattitude}'
        longitude_and_lattitude = url.replace(',', ', ')
        location = url

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

    return HttpResponse(template.render(context, request))