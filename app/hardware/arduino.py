from smbus import SMBus


class Arduino:
    """Arduino class used for sending bytes through an I2C serial connection"""

    def __init__(self, address):
        self.bus = SMBus(1)
        self.address = address

    def __del__(self):
        self.bus.close()

    def write(self, data):
        """Writes the specified bytes to the target Arduino"""
        # TODO: Use write_block / write_word
        for byte in data:
            self.bus.write_byte(self.address, byte)
