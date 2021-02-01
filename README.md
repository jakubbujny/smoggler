# WIP
Project is currently work-in-progress so README info might not be accurate

# Smoggler
Air quality measurement tool based on RPI and SDS011. It exposes website which can be reached
in LAN to display air quality with historical data.

All state is stored in mem so power off = historical data lost.

# Requirements
* Raspberry PI (tested with RPI3 B, Raspbian Buster Lite)
* Nova Fitness SDS011 
* USB-UART Converter

# Installation guide

# Implementation
Backend Python3. 
Frontend JQuery + Chart.js

Integration with SDS011 is based on https://github.com/ikalchev/py-sds011 
