from bs4 import BeautifulSoup
import requests

class weatherParser:
    '''Weather Parser from drops.live'''

    __weather_host = 'https://www.drops.live'
    __current_weather = None

    def setUrl(self, url):
        self.__URL = url

    def __getURL(self):
        return self.__URL

    def __getDataWeatherRaw(self):
        try:
            return requests.get(self.__weather_host+ "/" +self.__getURL()).content
        except ConnectionError:
            return False

    def __setSoup(self, weather_data):
        self.__soup = BeautifulSoup(weather_data, 'html.parser')

    def __getSoup(self):
        return self.__soup

    def setWeatherData(self):
        weather_data = self.__getDataWeatherRaw()
        self.__setSoup(weather_data)
        self.__setCurrentWeather(self.__parseCurrentWeather())

    def getCurrentTemperature(self):
        return self.__parseCurrentTemperature()

    def getWeatherLocation(self):
        try:
            self.__soup 
            return self.__parseWeatherLocation()
        except AttributeError:
            return None

    def __setCurrentWeather(self, current_weather):
        self.__current_weather = current_weather

    def __getCurrentWeather(self):
        return self.__current_weather

    def __parseCurrentWeather(self):
        soup = self.__getSoup()
        if soup.select_one('.weather-now'):
            return soup.find(class_='weather-now')
        return None

    def __parseCurrentTemperature(self):
        if self.__current_weather != None:
            current_weather = self.__getCurrentWeather()
            if current_weather.select_one('.temp'):
                return self.__getCurrentWeather().find(class_='temp').text
        return None

    def getCurrentWeatherIcon(self):
        if self.__current_weather != None:
            parsed_icon = self.__parseCurrentWeatherIcon()
            if parsed_icon != None:
                return self.__weather_host + self.__parseCurrentWeatherIcon()
        return None

    def __parseCurrentWeatherIcon(self):
        current_weather = self.__getCurrentWeather()
        if current_weather.select_one('.icon.left'):
            return self.__getCurrentWeather().find(class_="icon left")['src']
        return None
    
    def __parseWeatherLocation(self):
        location = self.__getSoup().find(class_='location')
        return location.find(class_='city').text