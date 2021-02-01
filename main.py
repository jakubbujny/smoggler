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
if os.environ["DEV"] is not None:
    queueSize = cfg.config["dev"]["queueSize"]
    sensor = lib.sensor.MockedDynamicSensor(queueSize=cfg.config["dev"]["queueSize"], sleepTime=10, randomUpperRange=15.0, randomLowerRange=5.0)
else:
    queueSize = cfg.config["prod"]["queueSize"]
    sds = lib.sds011.SDS011("/dev/ttyUSB0")
    sensor = lib.sensor.Sensor(sdsConnection=sds, queueSize=cfg.config["prod"]["queueSize"], minutesToWaitBetweenMeasurements=1, secondsWhenSensorIsActivated=60)

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
    app.run()
