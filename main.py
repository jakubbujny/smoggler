import time

import lib.sds011
import lib.sensor

def main():
    sds = lib.sds011.SDS011("/dev/ttyUSB0")
    sensor = lib.sensor.Sensor(sdsConnection=sds, queueSize=3, minutesToWaitBetweenMeasurements=1, secondsWhenSensorIsActivated=60)
    sensor.startGatheringDataInBackground()
    while True:
        print(sensor.getAllAvailableData())
        time.sleep(15)


if __name__ == "__main__":
    main()
