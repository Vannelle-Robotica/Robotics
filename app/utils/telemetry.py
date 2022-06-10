import requests as rq
import time
import psutil

from app import Application
from app.hardware.loadcell import LoadCell
from app.utils import opencv

url = 'http://localhost:5217/upload'


def upload(data):
    return rq.post(url, data)


def get_temperature():
    # Read temperature from thermal zone 0
    file = open('/sys/class/thermal/thermal_zone0/temp')
    contents = file.readline()

    # Close file and return
    file.close()
    return float(contents) / 1000

def get_weight():
    weight = LoadCell.get_weight()
    return weight

def get_speed():
    # diameter = 105 mm
    # diameter * pi = distance
    distance = 0.3298 # m/s
    start = time.perf_counter() # sec
    #if angle == 360:
    stop = time.perf_counter()
    #else:
     #   exit()
    timebetween = stop - start
    speed = distance /timebetween
    return speed

def get_mode():
    mode = Application.currentMode

    return mode

def get_batterylvl():
    batterylvl = psutil.sensors_battery()
    batteryPersentage = str(batterylvl.percent)
    return batteryPersentage

def get_vacuumstatus():
    status = False
    if opencv.turn_to_object:
        status = True

    return status

# TODO: Add more data and use actual values from sensors
# data = {
#     'Mode': get_mode(),
#     'Temperature': get_temperature(),
#     'Weight': get_weight(),
#     'BatteryPersentage': get_batterylvl(),
#     'Speed': get_speed(),
#     'VacuumStatus': get_vacuumstatus()
# }

# response = rq.post(url, data)
# print(f'Upload response({response.status_code}): {response.reason}')
