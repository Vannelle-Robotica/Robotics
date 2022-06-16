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
        self.close = False
        self.on = False
        self.incr = 102
        self.decr = 930
        self.decr1 = 950

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

    # def toggle_wheels(self):
    #     """Toggles the wheels between the open and closed state"""
    #     self.open = not self.open
    #     if self.open:
    #         self.write('0102')
    #         self.write('1102')
    #         self.write('2930')
    #         self.write('3950')
    #     else:
    #         self.write('0546')
    #         self.write('1546')
    #         self.write('2477')
    #         self.write('3477')

    def toggle_wheels(self, button):
        """Toggles the wheels between the open and closed state"""
        # change direction based on button pressed
        # get to the closest value of wheel max and minus values
        if button == 3:
            changeValue = 100
        else:
            changeValue = -100

        self.decr -= changeValue
        self.incr += changeValue
        for x in range(4):

            if self.incr > 546:
                self.incr = 546
            elif self.incr < 102:
                self.incr = 102
            if self.decr < 477:
                self.decr = 477
            elif self.decr > 930:
                self.decr = 930

            if x > 1:
                if x > 2:
                    self.write(str(x) + str(self.decr + 20))
                else:
                    self.write(str(x) + str(self.decr))
            self.write(str(x) + str(self.incr))

    def toggle_wheels_front(self):
        """Toggles the wheels between the open and closed state"""
        self.open = not self.open
        if self.open:
            self.write('0102')
            self.write('1102')
        else:
            self.write('0546')
            self.write('1546')


    def toggle_wheels_back(self):
        """Toggles the wheels between the open and closed state"""
        self.open = not self.open
        if self.open:
            self.write('2920')
            self.write('3920')
        else:
            self.write('2477')
            self.write('3477')


    def use_vaccuum(self):
        self.on = not self.on
        if self.on:
            self.write('50')
        else:
            self.write('50')
