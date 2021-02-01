# Smoggler
Air quality measurement tool based on RPI and SDS011. It exposes website which can be reached
in LAN to display air quality with historical data.

## Web
![alt text](https://github.com/jakubbujny/smoggler/blob/main/readme/web.png?raw=true)

## Mobile
![alt text](https://github.com/jakubbujny/smoggler/blob/main/readme/mobile.jpg?raw=true)

# Features
* Getting data from sensor
* Presenting last N points of data (configurable via queueSize) on chart
* Showing current value in chart's title
* State is stored in mem so power off = historical data lost.

# Requirements
* Raspberry PI (tested with RPI3 B, Raspbian Buster Lite)
* Nova Fitness SDS011 
* USB-UART Converter

# Installation guide

Dockerhub: https://hub.docker.com/r/jakubbujny/smoggler 

# Implementation
Backend Python3 together with sds011 library (https://pypi.org/project/sds011/).
Data from sensor lands in FIFO queue and is exposed as JSON via /sensor-data endpoint.
Frontend JQuery + Chart.js - simple ajax call + chart.

# TODO
* Live update of chart
* Change config via HTML form
