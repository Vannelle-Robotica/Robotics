import time
from threading import Thread

from bluepy import btle


# TODO: Refactor
class MyDelegate(btle.DefaultDelegate):

    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, handle, data):

        try:
            dataDecoded = data.decode()
            print(dataDecoded)
        except UnicodeError:
            print(f'UnicodeError: {data}')


class BLEClient:
    """"Bluetooth low energy client wrapper"""

    def __init__(self, addr):
        super().__init__()
        self.bytes_to_send = None
        self.rqs_to_send = False
        self.running = False

        # Connect and set delegate
        self.per = btle.Peripheral(addr)
        self.per.setDelegate(MyDelegate())

        # Initialize service and characteristic
        self.svc = self.per.getServiceByUUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
        self.ch = self.svc.getCharacteristics('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')[0]

        # Start client thread
        self.thread = Thread(target=self._run)
        self.thread.start()

    def __del__(self):
        # Disconnect from server
        self.per.disconnect()

    def _run(self):
        if self.running:
            return

        print('BLE Client started')
        self.running = True

        # Write to characteristics
        self.per.writeCharacteristic(self.ch.valHandle + 1, b"\x01\00")

        # BLE loop
        while True:
            # Wait for notification from ESP32
            self.per.waitForNotifications(1.0)

            if self.rqs_to_send:
                self.rqs_to_send = False

                try:
                    self.ch.write(self.bytes_to_send, True)
                except btle.BTLEException:
                    print('btle.BTLEException')
                    break

        # Print exit
        print('WorkerBLE end')

    def write(self, to_send):
        """Write the specified data to the server"""
        self.bytes_to_send = bytes(to_send, 'utf-8')
        self.rqs_to_send = True


# Initialize BLE client
client = BLEClient('78:E3:6D:10:2C:2E')

while True:
    # Write to server
    client.write('Hello world')

    time.sleep(0.5)
