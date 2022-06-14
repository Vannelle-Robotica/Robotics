import re
import time

import RPi.GPIO as GPIO
from bluepy import btle

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
        self.arduino = Arduino(0x8)

        # Initialize Magnet
        self.magnet = Magnet()

        try:
            # Attempt to connect to controller
            print('Waiting for controller')
            self.ble = BLEClient('78:E3:6D:10:C2:2E', self.on_receive)
        except btle.BTLEDisconnectError:
            print('Failed to connect')
            exit(1)
            pass

        # Initialize Motors
        self.motors = Motors()
        print('Connected')

    def __del__(self):
        if 'motors' in locals():
            self.motors.move('s', 0)

    def on_receive(self, data):
        match = re.search(r'^d (\w{1,2}) b ([0-6]) s (\d+)$', data)
        if match is None:
            print(f'Invalid data received: ({data})')
            return

        # TODO
        (direction, button, speed) = match.groups()
        speed = int(speed)
        # print(f'dir: {direction} button: {button} speed: {speed}')
        self.motors.move(direction, speed)
        self.motors.speed(speed)

        if button == '1':
            self.magnet.toggle_magnet()
        elif button == '2':
            self.arduino.toggle_arm()
        elif button == '3':
            self.arduino.toggle_wheels()
            print(f'button: {button}')
        elif button == '4':
            # TODO: Impl
            print('4')
        elif button == '5':
            # TODO: Impl
            print('5')
        elif button == '6':
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

        # weight = self.loadCells.get_combined_weight()
        # print(f'Weight: {weight}')
        # self.ble.write(str(weight))

        # TODO: Post telemetry data to website
        # upload(self.currentMode, weight)
        time.sleep(.5)

    def is_connected(self):
        return self.ble.is_connected()


# Entry point
def main():
    # Start application
    app = Application()

    # Update while connected to the controller
    try:
        while app.is_connected():
            app.update()
    except KeyboardInterrupt:
        pass

    # Cleanup on shutdown
    print('Disconnected')
    GPIO.cleanup()
    exit(0)


# Call entry point
if __name__ == '__main__':
    main()
