from django import template

register = template.Library()

@register.simple_tag
def weather_coordinates_url(value):
    return str(value).split(", ")
