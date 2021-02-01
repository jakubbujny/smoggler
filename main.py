import json
import os
import time

import lib.sds011
import lib.sensor
import lib.config

from flask import Flask, jsonify
app = Flask(__name__, static_folder='web',)

cfg = lib.config.Config("config.yaml")

sensor = None
queueSize = None
if "DEV" in os.environ:
    queueSize = cfg.config["dev"]["queueSize"]
    sensor = lib.sensor.MockedDynamicSensor(queueSize=cfg.config["dev"]["queueSize"], sleepTime=cfg.config["dev"]["sleepTime"], randomUpperRange=cfg.config["dev"]["randomUpperRange"], randomLowerRange=cfg.config["dev"]["randomLowerRange"])
else:
    queueSize = cfg.config["prod"]["queueSize"]
    sds = lib.sds011.SDS011("/dev/ttyUSB0")
    sensor = lib.sensor.Sensor(sdsConnection=sds, queueSize=cfg.config["prod"]["queueSize"], minutesToWaitBetweenMeasurements=cfg.config["prod"]["minutesToWaitBetweenMeasurements"], secondsWhenSensorIsActivated=cfg.config["prod"]["secondsWhenSensorIsActivated"])

sensor.startGatheringDataInBackground()


@app.route('/sensor-data')
def sensorData():
    resp = []
    for measurement in sensor.getAllAvailableData():
        resp.append({"timestamp":measurement.timestamp, "pm25": measurement.pm25, "pm10": measurement.pm10})
    return json.dumps({"measurements": resp, "queueSize": queueSize})

@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
