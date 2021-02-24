import datetime
import json
import logging
import queue
import random
import threading
import time


from abc import ABC, abstractmethod
import sds011

from lib.logger import logger


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


class Sensor(AbstractSensor):

    def __init__(self, sdsConnection: sds011.SDS011, queueSize:int, minutesToWaitBetweenMeasurements:int):
        self.sdsConnection = sdsConnection
        self.sdsConnection.set_working_period(rate=minutesToWaitBetweenMeasurements)
        self.measurementsQueue = queue.Queue(maxsize=queueSize)
        self.breakLoopLock = threading.Lock()

    def stop(self):
        logger.info("Stopping loop")
        self.breakLoopLock.acquire()
        logger.info("Stopped loop")

    def getAllAvailableData(self) -> [Measurement]:
        return list(self.measurementsQueue.queue)

    def startGatheringDataInBackground(self):
        logger.info("starting gathering data")
        self.thread = threading.Thread(target=self.__start, args=(self.sdsConnection, self.measurementsQueue, self.breakLoopLock))
        self.thread.start()

    def __start(self, sdsConnection: sds011.SDS011, queue:queue.Queue, breakLoopLock:threading.Lock):
        while not breakLoopLock.locked():
            meas = sdsConnection.read_measurement()

            if queue.full():
                queue.get()
            self.measurementsQueue.put(Measurement(int(datetime.datetime.now().timestamp()), meas["pm2.5"], meas["pm10"]))

    def setDelayBetweenMeasurements(self, minutesToWaitBetweenMeasurements):
        self.sdsConnection.set_working_period(rate=minutesToWaitBetweenMeasurements)

    def setNewQueueSize(self, size: int):
        logger.info("Acquiring lock")
        self.breakLoopLock.acquire()
        while self.thread.is_alive():
            logger.info("waiting for thread to stop")
            time.sleep(0.1)
        newQueue = queue.Queue(size)
        logger.info("copying queue")
        for el in list(self.measurementsQueue.queue):
            newQueue.put(el)
        self.measurementsQueue = newQueue
        logger.info("Releasing lock")
        self.breakLoopLock.release()
        self.startGatheringDataInBackground()

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
