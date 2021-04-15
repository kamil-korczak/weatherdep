from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Task Version
    # 2 URLS referencing to separate views
    path('temperature/zielona_gora', views.temperatureZG, name='zielona-gora'),
    # GS as Geographical Coordinates
    path('temperature/current/<longitude>,<lattitude>/', views.temperatureGC, name='other-location'),

    # Version 2
    # 2 URLs referencing to one view
    path('temperature2/zielona_gora', views.temperature2, name='zielona-gora2'),
    path('temperature2/current/<longitude>,<lattitude>/', views.temperature2, name='other-location2'),
]