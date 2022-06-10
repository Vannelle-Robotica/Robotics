import math
import requests as rq
import time
import psutil
from app import Application
from app.hardware import loadcell
from app.hardware.motors import Motors
from app.utils import opencv

url = 'http://localhost:5217/upload'

# Upload Data
def upload(data):
    return rq.post(url, data)

# Get Temperature from Raspberry Pi
def get_temperature():
    # Read temperature from thermal zone 0
    file = open('/sys/class/thermal/thermal_zone0/temp')
    contents = file.readline()

    # Close file and return
    file.close()
    return float(contents) / 1000

# Get Weight from the loadcells
def get_weight():
    weight = loadcell.get_weight(loadcell)
    return weight

# Get speed from the servomotors
def get_speed():
    diameter = 4.13386 # In Inches
    circumference = (diameter * math.pi) / 12 # In Feet
    revolutionsPerMile = 5280 / circumference
    speed = 255
    rpmRatio = 1.5
    maxRpm = 310 / rpmRatio # RPM of full capacity
    currentRpm = maxRpm * speed / 255
    milesPerHour = (currentRpm / revolutionsPerMile) * 60
    kilometerPerHour = milesPerHour * 1.609
    meterperseconde = kilometerPerHour / 3.6

    return meterperseconde

# Get operation mode
def get_mode():
    mode = Application.currentMode

    return mode

# Get battery capacity
def get_batterylvl():
    batterylvl = psutil.sensors_battery()
    batteryPersentage = str(batterylvl.percent)
    return batteryPersentage

# Get the state of the vacuumcleaner
def get_vacuumstatus():
    status = False
    if opencv.turn_to_object:
        status = True

    return status

data = {
    'Mode': get_mode(),
    'Temperature': get_temperature(),
    'Weight': get_weight(),
    'BatteryPercentage': get_batterylvl(),
    'Speed': get_speed(),
    'VacuumStatus': get_vacuumstatus()
}

response = rq.post(url, data)
print(f'Upload response({response.status_code}): {response.reason}')
