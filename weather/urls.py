from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # Task Version
    # 2 URLS referencing to separate views
    path('temperature/zielona_gora',
         views.TemperatureZielonaGora.as_view(), name='zielona-gora'),
    # GS as Geographical Coordinates
    path('temperature/current/<longitude>,<lattitude>/',
         views.TemperatureByGeographicalCordinates.as_view(), name='other-location'),

    # Version 2
    # 2 URLs referencing to one view
    path('temperature2/zielona_gora',
         views.TemperatureCombined.as_view(), name='zielona-gora2'),
    path('temperature2/current/<longitude>,<lattitude>/',
         views.TemperatureCombined.as_view(), name='other-location2'),

    # urls for polish terytory
    path('temperature/country/<country>/<voivodeship>/<county>/',
         views.TemperatureByCounty.as_view(), name='county'),
    path('temperature/country/<country>/<voivodeship>/',
         views.TemperatureByVoivodeship.as_view(), name='voivodeship'),
    path('temperature/country/<country>/',
         views.TemperatureByCountry.as_view(), name='country')

]
