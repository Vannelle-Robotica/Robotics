import RPi.GPIO as GPIO
from hx711 import HX711


class LoadCells:

	def __init__(self):
		# Set pinmode to BCM
		GPIO.setmode(GPIO.BCM)

		# Initialize LoadCells
		self.leftCell = LoadCell(-366, 19, 26)
		self.rightCell = LoadCell(-378.3, 20, 21)

	def get_combined_weight(self):
		return self.leftCell.get_weight() + self.rightCell.get_weight()


class LoadCell:

	def __init__(self, ratio, dout, pd):
		self.hx = HX711(dout_pin=dout, pd_sck_pin=pd)
		self.hx.set_scale_ratio(ratio)
		self.hx.zero()

	def get_weight(self):
		return round(self.hx.get_weight_mean(readings=20), 1)
