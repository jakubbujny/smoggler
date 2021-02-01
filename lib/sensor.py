import queue
import threading
import time
import typing

from lib.sds011 import SDS011, InvalidResponseFromDevice

class Measurement:

    def __init__(self, timestamp:int, pm25:float, pm10:float):
        self.timestamp = timestamp
        self.pm25 = pm25
        self.pm10 = pm10

    def __str__(self):
        return f"t:{self.timestamp} pm25:{self.pm25} pm10: {self.pm10}"

    def __repr__(self):
        return self.__str__()

class Sensor:

    def __init__(self, sdsConnection: SDS011, queueSize:int, minutesToWaitBetweenMeasurements:int, secondsWhenSensorIsActivated:int):
        self.sdsConnection = sdsConnection
        self.measurementsQueue = queue.Queue(maxsize=queueSize)
        self.minutesToWaitBetweenMeasurements = minutesToWaitBetweenMeasurements
        self.secondsWhenSensorIsActivated = secondsWhenSensorIsActivated

    def getAllAvailableData(self) -> [Measurement]:
        return list(self.measurementsQueue.queue)

    def startGatheringDataInBackground(self):
        thread = threading.Thread(target=self.__start, args=(self.sdsConnection, self.measurementsQueue, self.minutesToWaitBetweenMeasurements, self.secondsWhenSensorIsActivated, ))
        thread.start()

    def __start(self, sdsConnection: SDS011, queue:queue.Queue, minutesToWaitBetweenMeasurements:int, secondsWhenSensorIsActivated:int):
        first = True
        while True:
            try:
                pm25, pm10 = sdsConnection.queryPM(secondsWhenSensorIsActivated)
            except InvalidResponseFromDevice:
                print("Received bad response from device, sleep and retry")
                time.sleep(10)
                continue

            # For some unknown reason the first measurement seems to be always invalid so let's skip it
            if first:
                first = False
                continue

            if queue.full():
                queue.get()
            self.measurementsQueue.put(Measurement(0, pm25, pm10))
            time.sleep(minutesToWaitBetweenMeasurements*60)

