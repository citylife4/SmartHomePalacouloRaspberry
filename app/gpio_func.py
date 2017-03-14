import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library
import math

trig_pin = 23  # Associate pin 23 to TRIG
echo_pin = 24  # Associate pin 24 to ECHO
temperature = 10

DoorTrigger = 21


def setup_gpio() :
    # set GPIO pins
    GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering


def trigger_door() :
    GPIO.setup(DoorTrigger, GPIO.OUT)
    GPIO.output(DoorTrigger, False)
    time.sleep(1)
    GPIO.output(DoorTrigger, True)
    GPIO.cleanup(DoorTrigger)

'''
Return an error corrected unrounded distance, in cm, of an object
adjusted for temperature in Celcius.  The distance calculated
is the median value of a sample of `sample_size` readings.

Speed of readings is a result of two variables.  The sample_size
per reading and the sample_wait (interval between individual samples).
Example: To use a sample size of 5 instead of 11 will increase the
speed of your reading but could increase variance in readings;
value = sensor.Measurement(trig_pin, echo_pin)
r = value.raw_distance(sample_size=5)

Adjusting the interval between individual samples can also
increase the speed of the reading.  Increasing the speed will also
increase CPU usage.  Setting it too low will cause errors.  A default
of sample_wait=0.1 is a good balance between speed and minimizing
CPU usage.  It is also a safe setting that should not cause errors.

e.g.
r = value.raw_distance(sample_wait=0.03)

https://github.com/alaudet/hcsr04sensor
'''


def get_distance_boolean(sample_size=11, sample_wait=0.1, distance_to_door=10):
    speed_of_sound = 331.3 * math.sqrt(1 + (temperature / 273.15))
    sample = []
    # setup input/output pins
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    for distance_reading in range(sample_size):

        GPIO.output(trig_pin, GPIO.LOW)
        time.sleep(sample_wait)
        GPIO.output(trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(trig_pin, False)
        echo_status_counter = 1

        while GPIO.input(echo_pin) == 0:
            if echo_status_counter < 1000:
                sonar_signal_off = time.time()
                echo_status_counter += 1
            else:
                raise SystemError('Echo pulse was not received')
        while GPIO.input(echo_pin) == 1:
            sonar_signal_on = time.time()

        time_passed = sonar_signal_on - sonar_signal_off
        distance_cm = time_passed * ((speed_of_sound * 100) / 2)
        sample.append(distance_cm)
    sorted_sample = sorted(sample)

    # Only cleanup the pins used to prevent clobbering
    # any others in use by the program
    GPIO.cleanup((trig_pin, echo_pin))

    distance = sorted_sample[sample_size // 2]
    return distance, distance < distance_to_door
