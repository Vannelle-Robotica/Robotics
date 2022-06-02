import requests as rq

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

# TODO: Add more data and use actual values from sensors
# data = {
#     'Mode': 0,
#     'Temperature': 90,
#     'Weight': 10
# }

# response = rq.post(url, data)
# print(f'Upload response({response.status_code}): {response.reason}')
