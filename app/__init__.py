import re
import time

import RPi.GPIO as GPIO

from hardware.arduino import Arduino
from hardware.loadcell import LoadCells
from hardware.motors import Motors
from utils.ble import BLEClient
from utils.telemetry import get_temperature


class Application:

    def __init__(self):
        # Initialize LoadCells
        print('Initializing LoadCells')
        self.loadCells = LoadCells()

        # Initialize Arduino connection
        print('Initializing Arduino connection')
        self.arduino = Arduino('0x8')

        # Initialize Motors
        self.motors = Motors()

        # Attempt to connect to controller
        print('Waiting for controller')

        while True:
            try:
                self.ble = BLEClient('78:E3:6D:10:C2:2E', self.on_receive)
                break
            except:
                pass
        print('Connected')

    def on_receive(self, data):
        match = re.search(r'^d (\w+) b ([0-6]) s (\d+)$', data)
        if match is None:
            print(f'Invalid data received: ({data})')
            return

        # TODO
        (direction, button, speed) = match.groups()
        print(f'dir: {direction} button: {button} speed: {speed}')
        self.motors.Move(direction, int(speed))
        self.motors.speed(int(speed))

    def update(self):
        weight = self.loadCells.get_combined_weight()

        print(f'Weight: {weight}')
        self.ble.write(str(weight))
        print(f'Temperature: {get_temperature()}')
        time.sleep(.5)

    def is_connected(self):
        return self.ble.is_connected()


# Entry point
def main():
    # Start application
    app = Application()

    # Update while connected to the controller
    while app.is_connected():
        app.update()

    # Cleanup on shutdown
    print('Disconnected')
    GPIO.cleanup()


# Call entry point
if __name__ == '__main__':
    main()
