#!/bin/bash

# Update system
sudo apt update
sudo apt upgrade

# Install dependencies using pip
pip install opencv-python bluepy smbus

# Move bluetooth service override to override directory
sudo mkdir -p /etc/systemd/system/bluetooth.service.d/
sudo mv -b override.conf /etc/systemd/system/bluetooth.service.d/

# Enable bluetooth service and (re)start
sudo systemctl enable bluetooth
sudo systemctl restart bluetooth
