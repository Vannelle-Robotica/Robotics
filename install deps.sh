# Update system and install required packages
sudo pacman -Syu
sudo pacman --needed -S gcc bluez bluez-utils python-pip

# Install OpenCV and PyBluez from github because of a few crucial fixes
pip install opencv-python git+https://github.com/pybluez/pybluez

# Move bluetooth service override to override directory
# TODO: sudo mv -b override.conf /etc/systemd/system/bluetooth.service.d/

# Enable bluetooth service and (re)start
sudo systemctl enable bluetooth
sudo systemctl restart bluetooth
