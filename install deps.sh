#!/bin/bash

# Update system and install required packages
sudo pacman -Syu
sudo pacman --needed -S bluez bluez-utils python-pip

# Install OpenCV and BluePy using pip
pip install opencv-python bluepy

# Move bluetooth service override to override directory
sudo mkdir -p /etc/systemd/system/bluetooth.service.d/
sudo mv -b override.conf /etc/systemd/system/bluetooth.service.d/

# Enable bluetooth service and (re)start
sudo systemctl enable bluetooth
sudo systemctl restart bluetooth
