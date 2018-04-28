# Thanks to PyImageSearch this saved the hasles of getting openCV to work on Python of RPi3, tried to apt-get python-opencv at the very end, instead of following the tutorial
## https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/

setxkbmap -layout us ## change keyobard for tilde, double inverted and hash

## fetch em'
sudo apt-get update
sudo apt-get upgrade
sudo rpi-update
sudo reboot
sudo raspi-config  # expand file system here
sudo reboot
df -h  #to check the expanded file system
sudo apt-get purge wolfram-engine
sudo apt-get purge libreoffice*
sudo apt-get clean
sudo apt-get autoremove
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python2.7-dev python3-dev
sudo pip install imutils
sudo apt-get install python-opencv
sudo apt-get install libjpeg8-dev
sudo pip install --upgrade pip
sudo pip install --upgrade google-api-python-client
sudo pip install --upgrade Pillow
sudo pip install imutils
