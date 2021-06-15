from django.db.models import Subquery
from django.http.response import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import resolve
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .include import decorators
from .include.views import functions
from .models import Temperature

# test location  '52.044712511740244,15.621827286963514'
# test location - error '1000.99999999,20000.99999'

# http://192.168.1.3:9005/temperature/zielona_gora
# http://192.168.1.3:9005/temperature/current/32.044712511740244,15.621827286963514/


URL_ZIELONA_GORA = 'zielona-góra-zielona-góra-poland/51.93548,15.50643'


class IndexView(TemplateView):

    def get(self, request):
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

        weather_objects = Temperature.objects.filter(
            pk__in=Subquery(
                Temperature.objects.filter(**query_kwargs)
                .order_by('city__name', '-downloaded')
                .distinct('city__name').values('pk')
            )
        ).order_by('-downloaded')[:100]

        if not weather_objects:
            weather_objects = None

        return render(request, template_name='weather/index.html',
                      context={"weather_objects": weather_objects})


class TemperatureZielonaGora(TemplateView):
    def get(self, request):
        '''(Task Version) View responsible for displaying \
        temperature of Zielona Góra.'''

        past_week = functions.get_past_week(request)

        return render(request, template_name='weather/temperature.html',
                      context=functions.get_temperature_context_data_by_url(
                          url=URL_ZIELONA_GORA, past_week=past_week))


class TemperatureByGeographicalCordinates(TemplateView):
    def get(self, request, longitude=False, lattitude=False):
        '''(Task Version) View responsible for displaying \
        temperature based on geographical coordinates.'''

        past_week = functions.get_past_week(request)

        context = functions.get_temperature_context_data_by_url(
            url=f'{longitude},{lattitude}', past_week=past_week)

        if f'{longitude}, {lattitude}' != context['longitude_and_lattitude']:
            coordinates_splited = context['longitude_and_lattitude'].split(
                ', ')
            return redirect('other-location',
                            longitude=coordinates_splited[0],
                            lattitude=coordinates_splited[1])

        return render(request, template_name='weather/temperature.html', context=context)


class TemperatureCombined(TemplateView):

    def get(self, request, longitude=False, lattitude=False):
        '''(Version 2) View of combined views responsible for displaying temperature:
        * of Zielona Góra
        * and based on geographical coordinates.'''

        current_url = resolve(request.path_info).url_name

        past_week = functions.get_past_week(request)

        if current_url == 'zielona-gora2':
            url = URL_ZIELONA_GORA
        elif current_url == 'other-location2':
            url = f'{longitude},{lattitude}'

        return render(request, template_name='weather/temperature.html',
                      context=functions.get_temperature_context_data_by_url(url, past_week))


class TemperatureByCountry(TemplateView):

    @method_decorator(decorators.iri_url)
    def get(self, request, country):

        if country.lower() == 'polska':

            past_week = functions.get_past_week(request)

            return render(request, template_name='weather/country.html',
                          context=functions.get_country_context(country, past_week))
        return HttpResponseNotFound(f"<h1>Page does not exist for {country}.</h1>")


class TemperatureByVoivodeship(TemplateView):

    @method_decorator(decorators.iri_url)
    def get(self, request, country, voivodeship):

        if country.lower() == 'polska':

            past_week = functions.get_past_week(request)

            return render(request, template_name='weather/voivodeship.html',
                          context=functions.get_voivodeship_context(country, voivodeship, past_week))
        return HttpResponseNotFound(f"<h1>Page does not exist for {country}.</h1>")


class TemperatureByCounty(TemplateView):

    @method_decorator(decorators.iri_url)
    def get(self, request, country, voivodeship, county):

        if country.lower() == 'polska':

            past_week = functions.get_past_week(request)

            return render(request, template_name='weather/county.html',
                          context=functions.get_county_context(
                              country, voivodeship, county, past_week))
        return HttpResponseNotFound(f"<h1>Page does not exist for {country}.</h1>")
