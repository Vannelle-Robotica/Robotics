# Update system and install required packages
sudo pacman -Syu
sudo pacman --needed -S bluez-utils opencv-python

# Install PyBluez from github because of a few crucial fixes
pip install git+https://github.com/pybluez/pybluez

# TODO: Ask to override bluetooth service

# Move bluetooth service override to override directory
sudo mv -b override.conf /etc/systemd/system/bluetooth.service.d/

# Enable bluetooth service and (re)start
sudo systemctl enable bluetooth
sudo systemctl restart bluetooth