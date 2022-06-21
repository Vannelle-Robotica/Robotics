import re
import time

from bluepy import btle

from hardware.arduino import Arduino
from hardware.loadcell import LoadCells
from hardware.magnet import Magnet
from hardware.motors import Motors
from utils.ble import BLEClient
from utils.opencv import *
from utils.operatingmode import OperatingMode
from utils.telemetry import upload


TURN_SPEED = 60


class Application:
    currentMode = OperatingMode.autonomous

    def __init__(self):
        # Initialize LoadCells
        print('Initializing LoadCells')
        self.loadCells = LoadCells()

        # Initialize Arduino connection
        print('Initializing Arduino connection')
        self.arduino = Arduino(0x8)

        # Initialize OpenCV
        self.camera = Camera()

        # Initialize Magnet
        self.magnet = Magnet()
        self.magnet.toggle_magnet()

        # Initialize Motors
        self.motors = Motors()

        while True:
            try:
                # Attempt to connect to controller
                print('Waiting for controller')
                self.ble = BLEClient('78:E3:6D:10:C2:2E', self.on_receive)
                print('Connected')
                break
            except btle.BTLEDisconnectError:
                print('Failed to connect')
                time.sleep(1)
                pass

    def __del__(self):
        if 'motors' in locals():
            self.motors.move('s')

    def on_receive(self, data):
        match = re.search(r'^d (\w{1,2}) m ([0-3]) b ([0-6]) s (\d+)$', data)
        if match is None:
            print(f'Invalid data received: ({data})')
            return

        # Parse received data
        (direction, mode, button, speed) = match.groups()
        self.currentMode = OperatingMode(int(mode))
        speed = int(speed)

        print(f'dir: {direction} mode: {mode} button: {button} speed: {speed}')
        self.motors.move(direction, speed)

        if button == '1':
            self.magnet.toggle_magnet()
        elif button == '2':
            self.arduino.toggle_arm()
        elif button == '3':
            self.arduino.toggle_wheels()
        elif button == '4':
            self.arduino.toggle_wheels()
        elif button == '5':
            # TODO: Impl
            print('5')

    def update(self):
        if self.currentMode == OperatingMode.autonomous:
            contour, width = self.camera.get_object(BLUE_SQUARE, 160)
            width = width / 2

            if contour is not None:
                centroid = get_centroid(contour)

                # TODO: Move motors
                if centroid > width + 60:
                    #speed = max(centroid - width - 30, 65)

                    self.motors.move('rr', TURN_SPEED)
                elif centroid < width - 60:
                    #speed = max(width - centroid - 30, 65)
                    self.motors.move('rl', TURN_SPEED)
                else:
                    print('No turn')
                    self.motors.move('s')
            else:
                self.motors.move('s')
        elif self.currentMode == OperatingMode.controlled:
            weight = self.loadCells.get_combined_weight()
            print(f'Weight: {weight} ')
            self.ble.write(str(weight))
            pass
        elif self.currentMode == OperatingMode.lineDance:
            pass
        elif self.currentMode == OperatingMode.dancing:
            pass

        # TODO: Post telemetry data to website
        # upload(self.currentMode, weight)
        # time.sleep(.5)

    def is_connected(self):
        return self.ble.is_connected()


# Entry point
def main():
    while True:
        # Start application
        app = Application()

        # Update while connected to the controller
        try:
            while app.is_connected():
                app.update()
        except btle.BTLEDisconnectError:
            print('Disconnected')
            pass
        except KeyboardInterrupt:
            break


# Call entry point
if __name__ == '__main__':
    main()
