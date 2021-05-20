from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import resolve

from .include.views import functions
from .models import Temperature

# test location  '52.044712511740244,15.621827286963514'
# test location - error '1000.99999999,20000.99999'

# http://192.168.1.3:9005/temperature/zielona_gora
# http://192.168.1.3:9005/temperature/current/32.044712511740244,15.621827286963514/


URL_ZIELONA_GORA = 'zielona-góra-zielona-góra-poland/51.93548,15.50643'


def index(request):
    """
    # filter usage:
    ?filter=<string_filter_name>&type=<string_filter_type>&value=<string_filter_value>
    # example:
    ?filter=temperature&type=lt&value=21
    """
    query_kwargs = {}

    if request.GET:
        string_filter_name = request.GET.get('filter', "")
        string_filter_type = request.GET.get('type', "")
        string_filter_value = request.GET.get('value', "")

        if string_filter_name != "" and \
                string_filter_type != "" and \
                string_filter_value != "":

            string_query_kwargs_key = f"{string_filter_name}__{string_filter_type}"
            query_kwargs[string_query_kwargs_key] = string_filter_value

    try:
        weather_objects = Temperature.objects.filter(
            **query_kwargs).order_by('-last_downloaded')
    except Temperature.DoesNotExist:
        weather_objects = None

    return render(request, template_name='weather/index.html',
                  context={"weather_objects": weather_objects})


def temperature_zielonga_gora(request):
    '''(Task Version) View responsible for displaying \
    temperature of Zielona Góra.'''

    return render(request, template_name='weather/temperature.html',
                  context=functions.get_temperature_context_data_by_url(
                      url=URL_ZIELONA_GORA))


def temperature_geographical_cordinates(request, longitude=False, lattitude=False):
    '''(Task Version) View responsible for displaying \
    temperature based on geographical coordinates.'''

    context = functions.get_temperature_context_data_by_url(
        url=f'{longitude},{lattitude}')

    if f'{longitude}, {lattitude}' != context['longitude_and_lattitude']:
        coordinates_splited = context['longitude_and_lattitude'].split(', ')
        return redirect('other-location',
                        longitude=coordinates_splited[0],
                        lattitude=coordinates_splited[1])

    return render(request, template_name='weather/temperature.html', context=context)


def temperature_combined(request, longitude=False, lattitude=False):
    '''(Version 2) View of combined views responsible for displaying temperature:
    * of Zielona Góra
    * and based on geographical coordinates.'''

    current_url = resolve(request.path_info).url_name

    if current_url == 'zielona-gora2':
        url = URL_ZIELONA_GORA
    elif current_url == 'other-location2':
        url = f'{longitude},{lattitude}'

    return render(request, template_name='weather/temperature.html',
                  context=functions.get_temperature_context_data_by_url(url))
