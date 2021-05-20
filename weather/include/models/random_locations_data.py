import random


class RandomLocationsData:
    """Get weather from random generated locations"""

    def __init__(self, temperature_class, count: int) -> None:
        self.temperature_class = temperature_class
        self.locations = []
        self.get_data(count)

    def generate_single_location(self) -> tuple:
        random_longitude = random.uniform(-90, 90.0)
        random_lattitude = random.uniform(-180, 180)
        new_location = (random_longitude, random_lattitude)

        if new_location in self.locations:
            self.generate_single_location()
        else:
            return new_location

    def get_data(self, count) -> None:

        while len(self.locations) < count:

            single_location = self.generate_single_location()

            longitude, lattitude = single_location

            counter = f"[{len(self.locations)+1}/{count}]"

            print(f"{counter} Trying get data for location {longitude, lattitude}")

            weather_data = self.temperature_class.objects.get_weather_data(
                url=f'{longitude},{lattitude}')

            print(weather_data)

            if weather_data['location']:
                self.temperature_class.objects.update_or_create_object(
                    weather_data)
                self.locations.append(single_location)
