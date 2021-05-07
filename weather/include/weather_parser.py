import requests
from bs4 import BeautifulSoup


class WeatherParser:
    '''Weather Parser from drops.live'''

    __weather_host = 'https://www.drops.live'
    __current_weather = None
    __soup = None
    __url = None

    def set_url(self, url):
        self.__url = url

    def __get_url(self):
        return self.__url

    def __get_data_weather_raw_data(self):
        try:
            return requests.get(
                self.__weather_host + "/" + self.__get_url(),
                headers={'User-Agent': 'Mozilla/5.0'}

                # TODO handle weather_data.status_code
                # for example status_code=502
            )
        except ConnectionError:
            print("ConnectionError")
            return False

    def __set_soup(self, weather_data):
        self.__soup = BeautifulSoup(weather_data, 'html.parser')

    def __get_soup(self):
        return self.__soup

    def set_weather_data(self):
        weather_data = self.__get_data_weather_raw_data()
        self.__set_soup(weather_data.content)
        self.__set_current_weather(self.__parse_current_weather())

    def get_current_temperature(self):
        return self.__parse_current_temperature()

    def get_weather_location(self):
        return self.__parse_weather_location()

    def __set_current_weather(self, current_weather):
        self.__current_weather = current_weather

    def __get_current_weather(self):
        return self.__current_weather

    def __parse_current_weather(self):
        soup = self.__get_soup()
        if soup.select_one('.weather-now'):
            return soup.find(class_='weather-now')
        return None

    def __parse_current_temperature(self):
        if self.__current_weather is not None:
            current_weather = self.__get_current_weather()
            if current_weather.select_one('.temp'):
                return int(self.__get_current_weather().find(class_='temp').text[:-1])
        return None

    def get_current_weather_icon(self):
        if self.__current_weather is not None:
            parsed_icon = self.__parse_current_weather_icon()
            if parsed_icon is not None:
                return parsed_icon
        return None

    def __parse_current_weather_icon(self):
        current_weather = self.__get_current_weather()
        if current_weather.select_one('.icon.left'):
            return self.__get_current_weather().find(class_="icon left")['src'][-12:-4]
        return None

    def __parse_weather_location(self):
        if self.__get_soup().select_one(".location"):
            location = self.__get_soup().find(class_='location')
            return location.find(class_='city').text
        return None
