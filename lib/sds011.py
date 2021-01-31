import struct
import time

import serial

class InvalidResponseFromDevice(Exception):
    pass

class SDS011():
    CMD_ID = b'\xb4'
    HEAD = b'\xaa'
    TAIL = b'\xab'

    QUERY_CMD = b"\x04"
    SLEEP_CMD = b"\x06"

    SLEEP = b"\x00"
    ACTIVE = b"\x01"


    def __init__(self, serial_port, baudrate=9600, timeout=2):
        self.serialPort = serial.Serial(port=serial_port, baudrate=baudrate, timeout=timeout)
        self.serialPort.flush()

    def getCommandHeader(self):
        return self.HEAD + self.CMD_ID

    def _getReplyFromDevice(self):
        raw = self.serialPort.read(size=10)
        data = raw[2:8]
        if len(data) == 0:
            raise InvalidResponseFromDevice("0 length")
        if (sum(d for d in data) & 255) != raw[8]:
            raise InvalidResponseFromDevice("invalid length")
        return raw

    def queryPM(self, waitingTime=45):
        self.active()
        time.sleep(waitingTime)
        cmd = self.HEAD + self.CMD_ID
        cmd += (self.QUERY_CMD
                + b"\x00" * 12)
        cmd = self.addChecksumAndID(cmd)
        self.serialPort.write(cmd)

        try:
            raw = self._getReplyFromDevice()
        finally:
            self.sleep()
        data = struct.unpack('<HH', raw[2:6])
        pm25 = data[0] / 10.0
        pm10 = data[1] / 10.0
        return pm25, pm10


    def sleep(self):
        cmd = self.getCommandHeader()
        cmd += (self.SLEEP_CMD
                + b"\x01"
                + self.SLEEP
                + b"\x00" * 10)
        cmd = self.addChecksumAndID(cmd)
        self.serialPort.write(cmd)
        self._getReplyFromDevice()

    def active(self):
        cmd = self.getCommandHeader()
        cmd += (self.SLEEP_CMD
                + b"\x01"
                + self.ACTIVE
                + b"\x00" * 10)
        cmd = self.addChecksumAndID(cmd)
        self.serialPort.write(cmd)
        self._getReplyFromDevice()

    def addChecksumAndID(self, cmd, id1=b"\xff", id2=b"\xff"):
        cmd += id1 + id2
        checksum = sum(d for d in cmd[2:]) % 256
        cmd += bytes([checksum]) + self.TAIL
        return cmd

