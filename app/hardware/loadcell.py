import RPi.GPIO as GPIO
from hx711 import HX711


class LoadCells:
    """Class used for managing the LoadCells used on the robot"""

    def __init__(self):
        # Set pinmode to BCM
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Initialize LoadCells
        self.leftCell = LoadCell(-2209.39, 24, 23)
        self.rightCell = LoadCell(-2189.69, 27, 22)

    def get_combined_weight(self):
        """Gets the combined weight of the left and right load cells"""
        return (self.leftCell.get_weight() + self.rightCell.get_weight()) * (2/3)


class LoadCell:

    def __init__(self, ratio, data_pin, clock_pin):
        self.hx = HX711(dout_pin=data_pin, pd_sck_pin=clock_pin)
        self.hx.set_scale_ratio(ratio)
        self.hx.zero()

    def get_weight(self):
        return round(self.hx.get_weight_mean(readings=20), 1)
