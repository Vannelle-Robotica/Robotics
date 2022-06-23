import time

import RPi.GPIO as GPIO

# GPIO Mode (BOARD / BCM). | GPIO.BCM lets you refer to only the usable gpio pins and not ground or vcc
GPIO.setmode(GPIO.BCM)

# set GPIO Pins.
GPIO_TRIGGER = 7
GPIO_ECHO = 8

# set pinmodes like in the arduino to input and output.
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


# There are four pins on the ultrasound module:
# VCC, GND, TRIG, ECHO
# connect a 330(or 1k) Ω resistor to ECHO then to a Pin
# through a 470(or 2k) Ω resistor you connect it also to GND.
# GPIO pins only tolerate maximal 3.3V the sensor works at 5V.
# Without the connection to ground the echo pin could give both 0 or 1 when inactive.

def distance():
    """Code to take distance data directly to raspberry Pi from ultra sonic distance sensors"""
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.0001)
    GPIO.output(GPIO_TRIGGER, False)

    # save StartTime by repeating until pi
    while GPIO.input(GPIO_ECHO) == 0:
        pass
    startTime = time.time()

    # refresh until signal received
    while GPIO.input(GPIO_ECHO) == 1:
        pass
    stopTime = time.time()

    # time difference between start and arrival
    timeElapsed = stopTime - startTime
    # multiply with the sonic speed (34300 cm/s)
    # in arduino you use 0.034 or /29 because arduino measures in milliseconds not seconds
    # and divide by 2 to account for travel direction.
    distanceCm = (timeElapsed * 34300) / 2

    return distanceCm


print(distance())
