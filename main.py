import json
import os
import requests
import yaml

import lib.sensor
import lib.config
import sds011

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
    sds = sds011.SDS011(cfg.config["prod"]["device"])
    sds.set_working_period(rate=cfg.config["prod"]["minutesToWaitBetweenMeasurements"])
    sensor = lib.sensor.Sensor(sdsConnection=sds, queueSize=cfg.config["prod"]["queueSize"])

sensor.startGatheringDataInBackground()


@app.route('/sensor-data')
def sensorData():
    resp = []
    for measurement in sensor.getAllAvailableData():
        resp.append({"timestamp":measurement.timestamp, "pm25": measurement.pm25, "pm10": measurement.pm10})
    return json.dumps({"measurements": resp, "queueSize": queueSize})

@app.route('/check-version')
def checkVersion():
    currentVersion = cfg.config["version"]
    r = requests.get("https://raw.githubusercontent.com/jakubbujny/smoggler/main/config.yaml", allow_redirects=True)
    downloaded = yaml.safe_load(r.content.decode("UTF-8"))
    if downloaded["version"] != currentVersion:
        return json.dumps({"version": "outdated"})

    return json.dumps({"version": "latest"})

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/icon.png')
def icon():
    return app.send_static_file('icon.png')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
