import time

from smbus import SMBus

addr = 0x8
bus = SMBus(1)

while True:
	byte = input("Input (0-255): ")

	bus.write_byte(addr, int(byte))
	time.sleep(.5)
