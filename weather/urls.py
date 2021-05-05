from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Task Version
    # 2 URLS referencing to separate views
    path('temperature/zielona_gora',
         views.temperature_zielonga_gora, name='zielona-gora'),
    # GS as Geographical Coordinates
    path('temperature/current/<longitude>,<lattitude>/',
         views.temperature_geographical_cordinates, name='other-location'),

    # Version 2
    # 2 URLs referencing to one view
    path('temperature2/zielona_gora',
         views.temperature_combined, name='zielona-gora2'),
    path('temperature2/current/<longitude>,<lattitude>/',
         views.temperature_combined, name='other-location2'),
]
