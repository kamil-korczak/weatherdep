class TemperatureColor:
    """Stores color and its range number."""
    min_: int
    max_: int
    color: str

    def __init__(self, min_: int, max_: int, color: str) -> None:
        self.min_n = min_
        self.max_n = max_
        self.color = color

    def in_range(self, color: int) -> bool:
        return self.min_n <= color <= self.max_n


def define_colors() -> list:
    """Return list of defined colors and their range numbers."""
    colors = [
        TemperatureColor(min_=25, max_=99, color='p25'),
        TemperatureColor(min_=23, max_=24, color='p23'),
        TemperatureColor(min_=20, max_=22, color='p20'),
        TemperatureColor(min_=17, max_=19, color='p17'),
        TemperatureColor(min_=14, max_=16, color='p14'),
        TemperatureColor(min_=11, max_=13, color='p11'),
        TemperatureColor(min_=8, max_=10, color='p8'),
        TemperatureColor(min_=5, max_=7, color='p5'),
        TemperatureColor(min_=3, max_=4, color='p3'),
        TemperatureColor(min_=0, max_=2, color='0'),
        TemperatureColor(min_=-2, max_=-1, color='m0'),
        TemperatureColor(min_=-4, max_=-3, color='m3'),
        TemperatureColor(min_=-7, max_=-5, color='m5'),
        TemperatureColor(min_=-9, max_=-8, color='m8'),
        TemperatureColor(min_=-12, max_=-10, color='m10'),
        TemperatureColor(min_=-15, max_=-13, color='m13'),
        TemperatureColor(min_=-18, max_=-16, color='m16'),
        TemperatureColor(min_=-24, max_=-19, color='m19'),
        TemperatureColor(min_=-99, max_=-25, color='m25'),
    ]
    return colors


def temperature_color(current_temperature) -> str:
    colors = define_colors()

    # method #1 using filter and lambda
    # result is list of objects
    # filtered_color = list(filter(lambda x: x.in_range(current_temperature), colors))

    # method #2 using Generator()
    # result is list of objects
    filtered_color = list((color for color in colors if color.in_range(
        current_temperature)))

    # method #3 using list
    # result is list of strings
    # filtered_color = [
    #     color.color for color in colors if color.in_range(current_temperature)]

    return filtered_color[0].color
