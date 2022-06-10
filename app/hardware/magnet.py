import RPi.GPIO as GPIO

pin = 4


class Magnet:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        self.state = False

    def toggle_magnet(self):
        self.state = not self.state
        if self.state:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)
