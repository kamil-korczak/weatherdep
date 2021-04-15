
def temperature_color(current_temperature):
    celsius_sign = '°'
    if current_temperature != None:
        ct = int(current_temperature.replace(celsius_sign, ''))
        if ct >= 25:
            return 'p25'
        elif ct >= 23 and ct <= 24:
            return 'p23'
        elif ct >= 20 and ct <= 22:
            return 'p20'
        elif ct >= 17 and ct <= 19:
            return 'p17'
        elif ct >= 14 and ct <= 16:
            return 'p14'
        elif ct >= 11 and ct <= 13:
            return 'p11'
        elif ct >= 8 and ct <= 10:
            return 'p8'
        elif ct >= 5 and ct <= 7:
            return 'p5'
        elif ct >= 3 and ct <= 4:
            return 'p3'
        elif ct >= 0 and ct <= 2:
            return '0'
        elif ct >= -2 and ct < 0:
            return 'm0'
        elif ct >= -4 and ct <= -3:
            return 'm3'
        elif ct >= -7 and ct <= -5:
            return 'm5'
        elif ct >= -9 and ct <= -8:
            return 'm8'
        elif ct >= -12 and ct <= -10:
            return 'm10'
        elif ct >= -15 and ct <= -13:
            return 'm13'
        elif ct >= -18 and ct <= -16:
            return 'm16'
        elif ct >= -24 and ct <= -19:
            return 'm19'
        else:
            return 'm25'
    return current_temperature