
def temperature_color(current_temperature):

    if current_temperature is not None:
        if current_temperature >= 25:
            return 'p25'
        elif current_temperature >= 23: #and current_temperature <= 24:
            return 'p23'
        elif current_temperature >= 20: #and current_temperature <= 22:
            return 'p20'
        elif current_temperature >= 17: # and current_temperature <= 19:
            return 'p17'
        elif current_temperature >= 14: # and current_temperature <= 16:
            return 'p14'
        elif current_temperature >= 11: # and current_temperature <= 13:
            return 'p11'
        elif current_temperature >= 8: # and current_temperature <= 10:
            return 'p8'
        elif current_temperature >= 5: # and current_temperature <= 7:
            return 'p5'
        elif current_temperature >= 3: # and current_temperature <= 4:
            return 'p3'
        elif current_temperature >= 0: # and current_temperature <= 2:
            return '0'
        elif current_temperature >= -2: # and current_temperature < 0:
            return 'm0'
        elif current_temperature >= -4: # and current_temperature <= -3:
            return 'm3'
        elif current_temperature >= -7: # and current_temperature <= -5:
            return 'm5'
        elif current_temperature >= -9: # and current_temperature <= -8:
            return 'm8'
        elif current_temperature >= -12: # and current_temperature <= -10:
            return 'm10'
        elif current_temperature >= -15: # and current_temperature <= -13:
            return 'm13'
        elif current_temperature >= -18: # and current_temperature <= -16:
            return 'm16'
        elif current_temperature >= -24: # and current_temperature <= -19:
            return 'm19'
        else:
            return 'm25'
    return current_temperature