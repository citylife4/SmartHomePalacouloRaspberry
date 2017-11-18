import GPIO.gpio_funcs

def decode_data(data):

    #TODO allway to if...
    if 'open' or 'close' in data:
        GPIO.gpio_funcs.trigger_door()
        print data
        return 'success_' + data
    elif 'distance' in data:
        return 'distance_' + GPIO.gpio_funcs.get_distance_boolean()
    else:
        return 'error'