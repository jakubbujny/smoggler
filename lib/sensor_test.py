import logging
import sys
import time
from unittest.mock import Mock

import pytest
from retry import retry

from lib.sds011 import SDS011
from lib.sensor import Sensor


def testValidSensorData():
    # given
    sdsMock = Mock(spec=SDS011)
    sdsMock.query.return_value = 10.0, 20.0
    sensor = Sensor(sdsMock, 5, 5, True)
    # when
    sensor.startGatheringDataInBackground()
    data = getDataFromSensor(sensor)
    sensor.stop()
    # then
    sdsMock.query.assert_called()
    assert data[0].pm25 == 10.0
    assert data[0].pm10 == 20.0


@retry(ValueError, tries=3, delay=1)
def getDataFromSensor(sensor: Sensor):
    if len(sensor.getAllAvailableData()) == 0:
        raise ValueError
    return sensor.getAllAvailableData()


def testSetNewQueueSize():
    # given
    sdsMock = Mock(spec=SDS011)

    def fn():
        time.sleep(0.5)
        return 10.0, 20.0
    sdsMock.query = fn
    sensor = Sensor(sdsMock, 15, 5, True)
    # when
    sensor.startGatheringDataInBackground()
    dataBefore = getDataFromSensor(sensor)
    sensor.setNewQueueSize(100)
    time.sleep(1)
    dataAfter = sensor.getAllAvailableData()
    sensor.stop()
    # then
    for pointBefore in dataBefore:
        assert pointBefore in dataAfter
    assert len(dataBefore) != len(dataAfter)
