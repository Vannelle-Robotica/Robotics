import re
import time

import RPi.GPIO as GPIO
import cv2

from app.utils.opencv import Camera
from hardware.arduino import Arduino
from hardware.loadcell import LoadCells
from hardware.magnet import Magnet
from hardware.motors import Motors
from utils.ble import BLEClient
from utils.operatingmode import OperatingMode
from utils.telemetry import upload


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

        # Initialize openCV
        Capture = cv2.VideoCapture
        self.camera = Camera(Capture)

        # initialize magnet
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

        if button == 1:
            self.magnet.toggle_magnet()
        elif button == 2:
            self.arduino.toggle_arm()
        elif button == 3:
            self.arduino.toggle_wheels()
        elif button == 4:
            # TODO: Impl
            print('4')
        elif button == 5:
            # TODO: Impl
            print('5')
        elif button == 6:
            self.currentMode = OperatingMode.next(self.currentMode)

    def update(self):
        if self.currentMode == OperatingMode.autonomous:
            pass
        elif self.currentMode == OperatingMode.controlled:
            pass
        elif self.currentMode == OperatingMode.lineDance:
            pass
        elif self.currentMode == OperatingMode.dancing:
            pass

        weight = self.loadCells.get_combined_weight()

        print(f'Weight: {weight}')
        self.ble.write(str(weight))

        # Post telemetry data to website
        upload(self.currentMode, weight)
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
