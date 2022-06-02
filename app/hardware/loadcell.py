import RPi.GPIO as GPIO
from hx711 import HX711


class LoadCells:
	"""Class used for managing the LoadCells used on the robot"""

	def __init__(self):
		# Set pinmode to BCM
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		# Initialize LoadCells
		self.leftCell = LoadCell(-366, 19, 26)
		self.rightCell = LoadCell(-378.3, 20, 21)

	def get_combined_weight(self):
		"""Gets the combined weight of the left and right loadcells"""
		return self.leftCell.get_weight() + self.rightCell.get_weight()


class LoadCell:

	def __init__(self, ratio, data_pin, clock_pin):
		self.hx = HX711(dout_pin=data_pin, pd_sck_pin=clock_pin)
		self.hx.set_scale_ratio(ratio)
		self.hx.zero()

	def get_weight(self):
		return round(self.hx.get_weight_mean(readings=20), 1)
