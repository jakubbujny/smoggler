import datetime
import json
import queue
import random
import threading
import time


from abc import ABC, abstractmethod
import sds011

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


class AbstractSensor(ABC):

    @abstractmethod
    def getAllAvailableData(self) -> [Measurement]:
        pass

    @abstractmethod
    def startGatheringDataInBackground(self):
        pass


class Sensor(AbstractSensor):

    def __init__(self, sdsConnection: sds011.SDS011, queueSize:int):
        self.sdsConnection = sdsConnection
        self.measurementsQueue = queue.Queue(maxsize=queueSize)
        self.breakLoopLock = threading.Lock()

    def stop(self):
        self.breakLoopLock.acquire()

    def getAllAvailableData(self) -> [Measurement]:
        return list(self.measurementsQueue.queue)

    def startGatheringDataInBackground(self):
        thread = threading.Thread(target=self.__start, args=(self.sdsConnection, self.measurementsQueue, self.breakLoopLock))
        thread.start()

    def __start(self, sdsConnection: sds011.SDS011, queue:queue.Queue, breakLoopLock:threading.Lock):
        while not breakLoopLock.locked():
            meas = sdsConnection.read_measurement()

            if queue.full():
                queue.get()
            self.measurementsQueue.put(Measurement(int(datetime.datetime.now().timestamp()), meas["pm2.5"], meas["pm10"]))


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
