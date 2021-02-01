import datetime
import queue
import random
import threading
import time

from abc import ABC, abstractmethod
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


class AbstractSensor(ABC):

    @abstractmethod
    def getAllAvailableData(self) -> [Measurement]:
        pass

    @abstractmethod
    def startGatheringDataInBackground(self):
        pass


class Sensor(AbstractSensor):

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


class MockedDynamicSensor(AbstractSensor):

    def __init__(self, queueSize:int, sleepTime:int, randomUpperRange:float, randomLowerRange:float):
        self.measurementsQueue = queue.Queue(maxsize=queueSize)
        self.sleepTime = sleepTime
        self.randomUpperRange = randomUpperRange
        self.randomLowerRange = randomLowerRange

    def getAllAvailableData(self) -> [Measurement]:
        return list(self.measurementsQueue.queue)

    def startGatheringDataInBackground(self):
        thread = threading.Thread(target=self.__start, args=(self.measurementsQueue, self.sleepTime, self.randomUpperRange, self.randomLowerRange))
        thread.start()

    def __start(self, queue:queue.Queue, sleepTime:int, randomUpperRange:float, randomLowerRange:float):
        while True:
            if queue.full():
                queue.get()
            self.measurementsQueue.put(Measurement(int(datetime.datetime.now().timestamp()), random.uniform(randomLowerRange, randomUpperRange), random.uniform(randomLowerRange, randomUpperRange)))
            time.sleep(sleepTime)
