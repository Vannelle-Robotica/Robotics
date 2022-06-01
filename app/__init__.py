import RPi.GPIO as GPIO

from hardware.loadcell import LoadCells
from utils.ble import BLEClient


class Application:

    def __init__(self):
        # Initialize LoadCells
        print('Initializing LoadCells')
        self.loadCells = LoadCells()

        # Initialize Servos
        print('Initializing Servos')
        # TODO

        # Attempt to connect to controller
        print('Waiting for controller')
        self.ble = BLEClient('78:E3:6D:10:C2:2E')
        print('Connected')

    def update(self):
        print('Application go brrr')

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
