# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import resolve
from .models import Temperature
from .include.functions_views import temperature_data
# Create your views here.

# test location  '52.044712511740244,15.621827286963514'
# test location - error '1000.99999999,20000.99999'

# http://192.168.1.3:9005/temperature/zielona_gora
# http://192.168.1.3:9005/temperature/current/32.044712511740244,15.621827286963514/


def index(request):
    template = loader.get_template('weather/index.html')

    try:
        weather_objects = Temperature.objects.all()
    except Temperature.DoesNotExist:
        weather_objects = None

    # weather_objects = None

    return HttpResponse(template.render(
        {"weather_objects": weather_objects},
        request))


def temperature_zielonga_gora(request):
    '''(Task Version) View responsible for displaying \
    temperature of Zielona Góra.'''
    template = loader.get_template('weather/temperature.html')

    url = 'zielona-góra-zielona-góra-poland/51.93548,15.50643'

    context = temperature_data(url)

    return HttpResponse(template.render(context, request))


def temperature_geographical_cordinates(request, longitude=False, lattitude=False):
    '''(Task Version) View responsible for displaying \
    temperature based on geographical coordinates.'''
    template = loader.get_template('weather/temperature.html')

    url = f'{longitude},{lattitude}'
    longitude_and_lattitude = url.replace(',', ', ')

    context = temperature_data(url, longitude_and_lattitude)

    return HttpResponse(template.render(context, request))


def temperature_combined(request, longitude=False, lattitude=False):
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

    context = temperature_data(url, longitude_and_lattitude)

    return HttpResponse(template.render(context, request))
