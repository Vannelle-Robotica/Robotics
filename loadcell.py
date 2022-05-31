import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setmode(GPIO.BCM)


class LoadCell:

	def __init__(self, ratio, dout, pd):
		self.hx = HX711(dout_pin=dout, pd_sck_pin=pd)
		self.hx.set_scale_ratio(ratio)
		self.hx.zero()

	def get_weight(self):
		return round(self.hx.get_weight_mean(readings=20), 1)


LEFT = LoadCell(-366, 19, 26)
RIGHT = LoadCell(-378.3, 20, 21)

try:
	while True:
		left = LEFT.get_weight()
		right = RIGHT.get_weight()

		print(f'{left}g + {right}g = {round(left + right, 1)}g')
finally:
	GPIO.cleanup()
