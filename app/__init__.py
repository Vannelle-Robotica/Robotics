import re
import time

import RPi.GPIO as GPIO

from hardware.arduino import Arduino
from hardware.loadcell import LoadCells
from hardware.magnet import Magnet
from hardware.motors import Motors
from utils.ble import BLEClient
from utils.operatingmode import OperatingMode
from utils.telemetry import get_temperature


class Application:
    currentMode = OperatingMode.controlled

    def __init__(self):
        # Initialize LoadCells
        print('Initializing LoadCells')
        self.loadCells = LoadCells()

        # Initialize Arduino connection
        print('Initializing Arduino connection')
        self.arduino = Arduino('0x8')

        # Initialize Motors
        self.motors = Motors()

        # initilize magnet
        self.magnet = Magnet()

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
        match = re.search(r'^d (\w{1,2}) b ([0-6]) s (\d+)$', data)
        if match is None:
            print(f'Invalid data received: ({data})')
            return

        # TODO
        (direction, button, speed) = match.groups()
        print(f'dir: {direction} button: {button} speed: {speed}')
        self.motors.move(direction, int(speed))
        self.motors.speed(int(speed))
        match button:
            case 1:
                self.magnet.toggle_magnet()
            case 2:
                self.arduino.moveArm()
            case 3:
                self.arduino.changeWeels()
            case 4:
                pass
            case 5:
                pass
            case 6:
                self.currentMode = OperatingMode.next(self.currentMode)

    def update(self):
        match self.currentMode:  # TODO: Add functionality to the different modes in this match case
            case OperatingMode.autonomous:
                pass
            case OperatingMode.controlled:
                pass
            case OperatingMode.lineDance:
                pass
            case OperatingMode.dancing:
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
