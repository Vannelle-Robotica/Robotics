# Robotics

This repository contains a python project that will be run on
a [Raspberry Pi 3b+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/). <br>
The script(s) will do the following:

- Control the [camera](https://www.raspberrypi.com/products/camera-module-v2/) attached to the pi
- Run computer vision code
- Handle the connection with the controller via bluetooth

And possible in the future:

- Communicate with the Arduino attached to the pi
- Control the wheels and/or robot arm

## Setup

### Linux

On [Arch](https://archlinux.org/)-based linux distributions the project can be set up by running
the [installation script](install%20deps.sh). <br>
On other distributions, you will have to install the following dependencies:

- [Bluez-utils](https://archlinux.org/packages/extra/x86_64/bluez-utils/)
- [python-opencv](https://archlinux.org/packages/extra/x86_64/python-opencv/) (or
  with [pip](https://pypi.org/project/opencv-python/))
- [pybluez](git+https://github.com/pybluez/pybluez) (with pip)

### Windows

Bluez is not supported on Windows, meaning you won't be able to use the controller. <br>
The remaining parts of this project require the following dependencies:

- [python-opencv](https://pypi.org/project/opencv-python/)
