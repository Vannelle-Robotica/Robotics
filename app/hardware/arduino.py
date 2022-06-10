from smbus import SMBus


def to_int_list(msg):
    """Converts the specified msg to a list of integers representing the ASCII chars"""
    return [ord(char) for char in msg]


class Arduino:
    """Arduino class used for sending bytes through an I2C serial connection"""

    def __init__(self, address):
        self.bus = SMBus(1)
        self.address = address
        self.down = False
        self.open = False
        self.on = False

    def __del__(self):
        self.bus.close()

    def write(self, msg):
        """Writes the specified msg to the target Arduino"""
        data = to_int_list(msg)
        self.bus.write_i2c_block_data(self.address, 0, data)

    def toggle_arm(self):
        """Toggles the arm between up and down"""
        self.down = not self.down
        if self.down:
            self.write('41023')  # TODO calculate exact amount of degrees needed to turn arm up or down
        else:
            self.write('40')

    def toggle_wheels(self):
        """Toggles the wheels between the open and closed state"""
        self.open = not self.open
        if self.open:
            self.write('0102')
            self.write('1102')
            self.write('2920')
            self.write('3920')
        else:
            self.write('0546')
            self.write('1546')
            self.write('2477')
            self.write('3477')

    def use_vaccuum(self):
        self.on = not self.on
        if self.on:
            self.write('50')  # TODO calculate exact amount of degrees needed to turn arm up or down
        else:
            self.write('40')
