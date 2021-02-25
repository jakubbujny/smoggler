# Smoggler
Air quality measurement tool based on RPI and SDS011. It exposes website which can be reached
in LAN to display air quality with historical data.

![alt text](https://github.com/jakubbujny/smoggler/blob/main/readme/web.png?raw=true)


# Features
* Getting data from sensor
* Presenting data on charts reachable via RPI's IP address
* Configurable history length
* Automated installation

# Requirements
* Raspberry PI (tested with RPI3 B, Raspbian Buster Lite)
* Nova Fitness SDS011 
* USB-UART Converter
* Internet connection 

# Installation guide

* Install fresh Raspbian on your RPI (https://www.raspberrypi.org/software/)
* Make sure your WIFI is configured with Internet access (https://www.raspberrypi.org/documentation/configuration/wireless/)
* Make sure you have root permissions (already logged as root or using sudo)
* Make sure SDS011 is already connected to RPI via USB  
* Open terminal and write command to run installation script
  
  ```curl -s https://raw.githubusercontent.com/jakubbujny/smoggler/main/install/install.sh | sudo bash```
* Run `ifconfig` command, in wlan0 interface find inet section so you can find RPI's IP address e.g. `inet 192.168.1.105`
* Open RPI's IP address in web browser e.g. `http://192.168.1.105`
* All done - enjoy!

# How to update?
Run the same steps as in `Installation guide`

# Config
Defaults
```
  queueSize: 144
  minutesToWaitBetweenMeasurements: 5
```
means 12h of history stored in-mem.

# Troubleshooting

## Device not found
If you see error like
```
Cannot start service smoggler: error gathering device information while adding custom device "/dev/ttyUSB0": no such file or directory
```
it means SDS011 is not found. Try to reconnect it and make again all steps from installation guide.

## Docker network
If you see error like
```
failed to add the host (vethXXX) <=> sandbox (vethYYY) pair interfaces: operation not supported
```
it means Docker cannot create network because of errors from Kernel. Restart RPI and run installation script once again.


# TODO
* Live update of chart
* Add push notifications to phones via IFTTT (https://medium.com/better-programming/how-to-send-push-notifications-to-your-phone-from-any-script-6b70e34748f6)
