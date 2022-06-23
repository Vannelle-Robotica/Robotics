import RPi.GPIO as GPIO
from hx711 import HX711


class LoadCells:
    """Class used for managing the LoadCells used on the robot"""

    def __init__(self):
        # Set pinmode to BCM
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Initialize LoadCells
        self.leftCell = LoadCell(-2209, 24, 23)
        self.rightCell = LoadCell(2195, 27, 22)

    def get_combined_weight(self):
        """Gets the combined weight of the left and right load cells"""
        return round((self.leftCell.get_weight() + self.rightCell.get_weight()) / 3 * 2, 1)


class LoadCell:

    def __init__(self, ratio, data_pin, clock_pin):
        self.hx = HX711(dout_pin=data_pin, pd_sck_pin=clock_pin)
        self.hx.set_scale_ratio(ratio)

        try:
            self.hx.zero()
            self.active = True
        except:
            print(f'Failed to initialize loadcell [{data_pin} - {clock_pin}]')
            self.active = False

    def get_weight(self):
        if not self.active:
            return -1
        # TODO: Fix
        return -2
        # return self.hx.get_weight_mean(readings=20)
