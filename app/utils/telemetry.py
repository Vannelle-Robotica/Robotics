import math

import psutil
import requests as rq

url = 'http://localhost:5217/upload'


# Upload Data
def upload(mode, weight):
    data = {
        'Mode': mode,
        'Temperature': get_temperature(),
        'Weight': weight,
        # 'BatteryPercentage': get_battery_lvl(),
        # 'Speed': get_speed(),
        # 'VacuumStatus': get_vacuum_status()
    }
    return rq.post(url, data)


# Get Temperature from Raspberry Pi
def get_temperature():
    # Read temperature from thermal zone 0
    file = open('/sys/class/thermal/thermal_zone0/temp')
    contents = file.readline()

    # Close file and return
    file.close()
    return float(contents) / 1000


# Get speed from the servomotors
def get_speed():
    # In Inches
    diameter = 4.13386

    # Calculate Circumference in feet
    circumference = (diameter * math.pi) / 12

    # Calculate revolutions per mile with the circumference
    revolutionsPerMile = 5280 / circumference

    # TODO: Get the current speed of the robot
    speed = 0  # Motors.speed()

    # RPM Gear ratio and calculating Max RPM using the gear ratio
    gearRatio = 1.5
    maxRpm = 310 / gearRatio

    # Calculating the current RPM with the speed and max RPM
    currentRpm = maxRpm * speed / 255

    # Calculating the speed in miles per hour and converting it to meters per second
    milesPerHour = (currentRpm / revolutionsPerMile) * 60
    meterperseconde = milesPerHour / 2.237

    return meterperseconde


# Get battery capacity
def get_battery_lvl():
    # Get battery level using the psutil library
    batterylvl = psutil.sensors_battery()
    batteryPercentage = str(batterylvl.percent)

    return batteryPercentage

# TODO: Get the state of the vacuum cleaner
# def get_vacuum_status():
#     status = False
#     if opencv.turn_to_object:
#         status = True
#
#     return status
