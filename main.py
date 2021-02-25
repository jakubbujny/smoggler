import json
import os

import requests
import yaml

import lib.sensor
import lib.config

from flask import Flask, render_template, send_from_directory, request, jsonify

from lib import sds011

app = Flask(__name__, static_folder='web',)

cfg = lib.config.Config("config.yaml")

sensor = None
queueSize = None
if "DEV" in os.environ and os.environ["DEV"] == "true":
    queueSize = cfg.config["dev"]["queueSize"]
    sensor = lib.sensor.MockedDynamicSensor(queueSize=cfg.config["dev"]["queueSize"], sleepTime=cfg.config["dev"]["sleepTime"], randomUpperRange=cfg.config["dev"]["randomUpperRange"], randomLowerRange=cfg.config["dev"]["randomLowerRange"])
else:
    queueSize = cfg.config["prod"]["queueSize"]
    sds = sds011.SDS011(cfg.config["prod"]["device"], use_query_mode=True)
    sensor = lib.sensor.Sensor(sdsConnection=sds, queueSize=cfg.config["prod"]["queueSize"], minutesToWaitBetweenMeasurements=cfg.config["prod"]["minutesToWaitBetweenMeasurements"])

sensor.startGatheringDataInBackground()


@app.route('/sensor-data')
def sensorData():
    resp = []
    for measurement in sensor.getAllAvailableData():
        resp.append({"timestamp":measurement.timestamp, "pm25": measurement.pm25, "pm10": measurement.pm10})
    return json.dumps({"measurements": resp})

@app.route('/check-version')
def checkVersion():
    currentVersion = cfg.config["version"]
    r = requests.get("https://raw.githubusercontent.com/jakubbujny/smoggler/main/config.yaml")
    downloaded = yaml.safe_load(r.content.decode("UTF-8"))
    if downloaded["version"] != currentVersion:
        return json.dumps({"version": "outdated"})

    return json.dumps({"version": "latest"})

@app.route('/config-data')
def configData():
    return json.dumps(cfg.config)

@app.route('/config-save', methods=['POST'])
def configSave():
    requestData = request.get_json()
    sensor.setNewQueueSize(requestData['queueSize'])
    sensor.setDelayBetweenMeasurements(requestData['minutesToWaitBetweenMeasurements'])
    cfg.config["prod"]["queueSize"] = requestData['queueSize']
    cfg.config["prod"]["minutesToWaitBetweenMeasurements"] = requestData['minutesToWaitBetweenMeasurements']
    cfg.saveConfig()
    return "ok"

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/config')
def config():
    return render_template('config.html')


@app.route('/icon.png')
def icon():
    return app.send_static_file('icon.png')


#disable cache
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(host='0.0.0.0')
