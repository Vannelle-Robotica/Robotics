import re
import time

import cv2
from bluepy import btle

from hardware.arduino import Arduino
from hardware.loadcell import LoadCells
from hardware.magnet import Magnet
from hardware.motors import Motors
from utils.ble import BLEClient
from utils.opencv import Camera, BLUE_SQUARE
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

        # Initialize OpenCV
        self.capture = cv2.VideoCapture(0)
        self.camera = Camera()

        # initialize Magnet
        self.magnet = Magnet()
        self.magnet.toggle_magnet()

        while True:
            try:
                # Attempt to connect to controller
                print('Waiting for controller')
                self.ble = BLEClient('78:E3:6D:10:C2:2E', self.on_receive)
                break
            except btle.BTLEDisconnectError:
                print('Failed to connect')
                time.sleep(1)
                pass

        # Initialize Motors
        self.motors = Motors()
        print('Connected')

    def __del__(self):
        if 'motors' in locals():
            self.motors.move('s', 0)
        self.capture.release()

    def on_receive(self, data):
        match = re.search(r'^d (\w{1,2}) b ([0-6]) s (\d+)$', data)
        if match is None:
            print(f'Invalid data received: ({data})')
            return

        # TODO
        (direction, button, speed) = match.groups()
        speed = int(speed)
        print(f'dir: {direction} button: {button} speed: {speed}')
        self.motors.move(direction, speed)
        self.motors.speed(speed)

        if button == '1':
            self.magnet.toggle_magnet()
        elif button == '2':
            self.arduino.toggle_arm()
        elif button == '3':
            self.arduino.toggle_wheels()  # button
        elif button == '4':
            self.arduino.toggle_wheels()
        elif button == '5':
            # TODO: Impl
            print('5')
        elif button == '6':
            self.currentMode = OperatingMode.next(self.currentMode)

    def update(self):
        if self.currentMode == OperatingMode.autonomous:
            ret, frame = self.capture.read()

            if ret is True:
                self.camera.get_object(frame, BLUE_SQUARE, 2, self.motors, self.arduino)
        elif self.currentMode == OperatingMode.controlled:
            pass
        elif self.currentMode == OperatingMode.lineDance:
            pass
        elif self.currentMode == OperatingMode.dancing:
            pass

        Weight = self.loadCells.get_combined_weight()
        print(f'Weight: {Weight} ')
        self.ble.write(str(Weight))

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


# Call entry point
if __name__ == '__main__':
    main()
