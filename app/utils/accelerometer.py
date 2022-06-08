from smbus import SMBus
import math

# Hiervoor moeten meer dingen worden geinstalleerd op de pi staat in de aantekeningen op discord
# nodig: sudo apt-get install i2c-tools python-smbus

# Register power management
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
address = 0x68  # via i2c detect run: sudo i2cdetect -y 1 to find address
bus = SMBus(1)


def init_gyro():
    # Activate the module so we can talk to it because it starts in sleepmode
    bus.write_byte_data(address, power_mgmt_1, 0)


def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg + 1)
    value = (h << 8) + l
    return value


def read_word_2c(reg):
    val = read_word(reg)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def get_z_direction():  # Gets the rotation of the gyroscope on the flat plane the robot drives on.
    gyro_zout = read_word_2c(0x47)
    return gyro_zout


def get_speed():  # Gets the current forward moving speed given the accelerometer is oriented correctly
    return read_word_2c(0x3d)

# Can add more for interesting telemetry data
