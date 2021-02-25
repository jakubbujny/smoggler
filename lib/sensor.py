import datetime
import json
import logging
import queue
import random
import threading
import time


from abc import ABC, abstractmethod

from lib.logger import logger
from lib.sds011 import SDS011


class Measurement:

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, timestamp:int, pm25:float, pm10:float):
        self.timestamp = timestamp
        self.pm25 = pm25
        self.pm10 = pm10

    def __str__(self):
        return f"t:{self.timestamp} pm25:{self.pm25} pm10: {self.pm10}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.timestamp == other.timestamp and self.pm25 == other.pm25 and self.pm10 == other.pm10:
            return True
        return False

class AbstractSensor(ABC):

    @abstractmethod
    def getAllAvailableData(self) -> [Measurement]:
        pass

    @abstractmethod
    def startGatheringDataInBackground(self):
        pass

    @abstractmethod
    def setNewQueueSize(self, size: int):
        pass

    @abstractmethod
    def setDelayBetweenMeasurements(self, delay: int):
        pass

class MeasurementConfiguration:

    def __init__(self, sdsConnection: SDS011, queue:queue.Queue, minutesToWaitBetweenMeasurements:int, breakLoopLock:threading.Lock, tests:bool):
        self.sdsConnection = sdsConnection
        self.queue = queue
        self.minutesToWaitBetweenMeasurements = minutesToWaitBetweenMeasurements
        self.breakLoopLock = breakLoopLock
        self.tests = tests


class Sensor(AbstractSensor):

    def __init__(self, sdsConnection: SDS011, queueSize:int, minutesToWaitBetweenMeasurements:int, tests=False):
        self.measurementConfiguration = MeasurementConfiguration(sdsConnection, queue.Queue(maxsize=queueSize), minutesToWaitBetweenMeasurements, threading.Lock(), tests)

    def stop(self):
        logger.info("Stopping loop")
        self.measurementConfiguration.breakLoopLock.acquire()
        logger.info("Stopped loop")

    def getAllAvailableData(self) -> [Measurement]:
        return list(self.measurementConfiguration.queue.queue)

    def startGatheringDataInBackground(self):
        logger.info("starting gathering data")
        self.thread = threading.Thread(target=self.__start, args=(self.measurementConfiguration,))
        self.thread.start()

    def __start(self, measurementConfiguration:MeasurementConfiguration):
        while not measurementConfiguration.breakLoopLock.locked():
            measurementConfiguration.sdsConnection.sleep(sleep=False)
            if not measurementConfiguration.tests:
                time.sleep(30)
            meas = measurementConfiguration.sdsConnection.query()
            measurementConfiguration.sdsConnection.sleep()
            if measurementConfiguration.queue.full():
                measurementConfiguration.queue.get()
            measurementConfiguration.queue.put(Measurement(int(datetime.datetime.now().timestamp()), meas[0], meas[1]))
            if not measurementConfiguration.tests:
                time.sleep((60*measurementConfiguration.minutesToWaitBetweenMeasurements)-30)

    def setDelayBetweenMeasurements(self, minutesToWaitBetweenMeasurements):
        self.measurementConfiguration.minutesToWaitBetweenMeasurements = minutesToWaitBetweenMeasurements

    def setNewQueueSize(self, size: int):
        newQueue = queue.Queue(size)
        logger.info("copying queue")
        for el in list(self.measurementConfiguration.queue.queue):
            if newQueue.full():
                newQueue.get()
            newQueue.put(el)
        self.measurementConfiguration.queue = newQueue

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

    def setNewQueueSize(self, size: int):
        pass

    def setDelayBetweenMeasurements(self, delay: int):
        pass
