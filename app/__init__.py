import enum
import re
import time

import RPi.GPIO as GPIO

from hardware.arduino import Arduino
from hardware.loadcell import LoadCells
from hardware.motors import Motors
from utils.ble import BLEClient
from utils.telemetry import get_temperature


class Modes(enum.Enum):
    autonomous = 0
    controlled = 1
    lineDance = 2
    dancing = 3

    def next(self):
        v = self.value
        if v == 3:
            return Modes(0)
        return Modes(v + 1)


class Application:
    currentMode = Modes.controlled

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
        if button == 6:
            self.currentMode = Modes.next(self.currentMode)
        if self.currentMode != Modes.controlled:
            self.motors.move(direction, int(speed))
            self.motors.speed(int(speed))

    def update(self):
        match self.currentMode:  # TODO: Add functionality to the different modes in this match case
            case Modes.autonomous:
                pass
            case Modes.controlled:
                pass
            case Modes.lineDance:
                pass
            case Modes.dancing:
                pass

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
