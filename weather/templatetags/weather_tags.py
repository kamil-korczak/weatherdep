from django import template
from weather.include.temperature_color import temperature_color

register = template.Library()


@register.simple_tag
def weather_coordinates_url(value):
    return str(value).split(", ")


@register.simple_tag
def weather_color_html_class(value):
    return temperature_color(value)


@register.simple_tag
def round_number(value):
    if value:
        return round(value, 2)
    return ''
