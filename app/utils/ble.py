from threading import Thread

from bluepy import btle


class Delegate(btle.DefaultDelegate):

    def __init__(self, on_receive):
        btle.DefaultDelegate.__init__(self)
        self.on_receive = on_receive

    def handleNotification(self, handle, data):
        try:
            decoded = data.decode()
            self.on_receive(decoded)
        except UnicodeError:
            print(f'UnicodeError: {data}')


class BLEClient:
    """"Bluetooth low energy client wrapper"""

    def __init__(self, addr, on_receive):
        super().__init__()
        self.bytes_to_send = None
        self.rqs_to_send = False
        self.running = False

        # Connect and set delegate
        self.per = btle.Peripheral(addr)
        self.per.setDelegate(Delegate(on_receive))

        # Initialize service and characteristic
        self.svc = self.per.getServiceByUUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
        self.ch = self.svc.getCharacteristics('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')[0]

        # Start client thread
        self.thread = Thread(target=self._run)
        self.thread.start()

    def __del__(self):
        # Disconnect from server
        if 'per' in locals():
            self.per.disconnect()

    def _run(self):
        """Handles the main update loop"""
        if self.running:
            return
        self.running = True

        # Initialize characteristics
        self.per.writeCharacteristic(self.ch.valHandle + 1, b"\x01\00")

        # BLE loop
        while self.is_connected():
            # Wait for notification from ESP32
            self.per.waitForNotifications(1.0)

            if self.rqs_to_send:
                self.rqs_to_send = False

                try:
                    # Write pending data to target device
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

    def is_connected(self):
        """Checks if the client is still connected to the server"""
        return True
        # return self.per.getState() == 'conn'
