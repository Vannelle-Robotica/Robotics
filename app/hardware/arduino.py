from smbus import SMBus


def to_int_list(msg):
    """Converts the specified msg to a list of integers representing the ASCII chars"""
    return [ord(char) for char in msg]


class Arduino:
    """Arduino class used for sending bytes through an I2C serial connection"""

    def __init__(self, address):
        self.bus = SMBus(1)
        self.address = address

    def __del__(self):
        self.bus.close()

    def write(self, msg):
        """Writes the specified msg to the target Arduino"""
        data = to_int_list(msg)
        self.bus.write_i2c_block_data(self.address, 0, data)
