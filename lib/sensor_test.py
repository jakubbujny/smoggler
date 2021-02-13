from unittest.mock import Mock

import sds011
from retry import retry

from lib.sensor import Sensor


def testValidSensorData():
    # given
    sdsMock = Mock(spec=sds011.SDS011)
    sdsMock.read_measurement.return_value = {"pm2.5": 10.0, "pm10": 20.0}
    sensor = Sensor(sdsMock, 5)
    # when
    sensor.startGatheringDataInBackground()
    data = getDataFromSensor(sensor)
    sensor.stop()
    # then
    sdsMock.read_measurement.assert_called()
    assert data[0].pm25 == 10.0
    assert data[0].pm10 == 20.0


@retry(ValueError, tries=3, delay=1)
def getDataFromSensor(sensor: Sensor):
    if len(sensor.getAllAvailableData()) == 0:
        raise ValueError
    return sensor.getAllAvailableData()

