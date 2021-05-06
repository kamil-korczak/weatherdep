class TemperatureColor:
    min_n: int
    max_n: int
    color: str

    def __init__(self, min_n: int, max_n: int, color: str) -> None:
        self.min_n = min_n
        self.max_n = max_n
        self.color = color

    def in_range(self, color: int) -> bool:
        return self.min_n <= color <= self.max_n


def define_colors() -> list:
    colors = [
        TemperatureColor(min_n=25, max_n=99, color='p25'),
        TemperatureColor(min_n=23, max_n=24, color='p23'),
        TemperatureColor(min_n=20, max_n=22, color='p20'),
        TemperatureColor(min_n=17, max_n=19, color='p17'),
        TemperatureColor(min_n=14, max_n=16, color='p14'),
        TemperatureColor(min_n=11, max_n=13, color='p11'),
        TemperatureColor(min_n=8, max_n=10, color='p8'),
        TemperatureColor(min_n=5, max_n=7, color='p5'),
        TemperatureColor(min_n=3, max_n=4, color='p3'),
        TemperatureColor(min_n=0, max_n=2, color='0'),
        TemperatureColor(min_n=-2, max_n=-1, color='m0'),
        TemperatureColor(min_n=-4, max_n=-3, color='m3'),
        TemperatureColor(min_n=-7, max_n=-5, color='m5'),
        TemperatureColor(min_n=-9, max_n=-8, color='m8'),
        TemperatureColor(min_n=-12, max_n=-10, color='m10'),
        TemperatureColor(min_n=-15, max_n=-13, color='m13'),
        TemperatureColor(min_n=-18, max_n=-16, color='m16'),
        TemperatureColor(min_n=-24, max_n=-19, color='m19'),
        TemperatureColor(min_n=-99, max_n=-25, color='m25'),
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
