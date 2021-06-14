from bs4 import BeautifulSoup
from .handle_requests import HandleRequests

WEATHER_HOST = 'https://www.drops.live'


def coordinates_str(url) -> any:
    if url:
        if url.find('/'):
            url = url[url.rfind('/')+1:]

        return url.replace(",", ", ")
    return None


class WeatherParser:
    '''Weather Parser from drops.live'''

    def __init__(self, url: str) -> None:
        self.__url = url
        self.__weather_data_raw = None
        self.__current_weather = None
        self.__soup = None
        self.set_weather_data()

    def __get_data_weather_raw(self) -> any:
        return HandleRequests.get(
            url=WEATHER_HOST + "/" + self.__url
        )

    def __set_soup(self) -> None:
        self.__soup = BeautifulSoup(
            self.__weather_data_raw.content, 'html.parser')

    def set_weather_data(self) -> None:
        self.__weather_data_raw = self.__get_data_weather_raw()
        self.__set_soup()
        self.__current_weather = self.__parse_current_weather()

    def __parse_current_weather(self) -> any:
        if self.__soup.select_one('.weather-now'):
            return self.__soup.find(class_='weather-now')
        return None

    def get_weather_url(self) -> any:
        if self.get_weather_location():
            return self.__weather_data_raw.url
        return None

    def get_current_temperature(self) -> any:
        if self.__current_weather:
            if self.__current_weather.select_one('.temp'):
                return int(self.__current_weather.find(class_='temp').text[:-1])
        return None

    def get_weather_location(self) -> any:
        if self.__soup.select_one(".location"):
            location = self.__soup.find(class_='location')
            return location.find(class_='city').text
        return None

    def get_current_weather_icon(self) -> any:
        if self.__current_weather:
            if self.__current_weather.select_one('.icon.left'):
                return self.__current_weather.find(class_="icon left")['src'][-12:-4]
        return None
