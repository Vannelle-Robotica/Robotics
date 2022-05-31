# Robotics

This repository contains a python project that will be run on
a [Raspberry Pi 3b+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/). <br>
The script(s) will do the following:

- Control the [camera](https://www.raspberrypi.com/products/camera-module-v2/) attached to the pi
- Run computer vision code
- Handle the connection with the controller via bluetooth
- Communicate with the Arduino attached to the pi

And possible in the future:

- Control the wheels and/or robot arm

## Setup

On [Raspberry Pi OS](https://www.raspberrypi.com/software/) the project can be set up by running
the [installation script](install%20deps.sh). <br>

If you aren't running Raspbian, you will need to manually install the following dependencies:
- [python-opencv](https://pypi.org/project/opencv-python/)
- [bluepy](https://pypi.org/project/bluepy/)
- [SMBus](https://pypi.org/project/SMBus/)
