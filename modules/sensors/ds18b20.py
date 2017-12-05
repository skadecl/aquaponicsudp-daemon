# DS18B20 Sensor
# Roberto Roman

#Remember to add w1-gpio and w1-therm to /etc/modules

import glob
import time

class DS18B20Sensor:
    id = None
    name = None
    deviceFile = None
    maxAttempts = None

    def __init__(self, pId, pName, pMaxAttempts):
        self.id = pId
        self.name = pName
        self.maxAttempts = pMaxAttempts

    def getDeviceFile(self):
        try:
            baseDir = '/sys/bus/w1/devices/'
            deviceFolder = glob.glob(baseDir + '28*')[0]
            self.deviceFile = deviceFolder + '/w1_slave'
        except Exception as e:
            self.deviceFile = False

    def readRawTemp(self):
        self.getDeviceFile()
        if self.deviceFile:
            try:
                f = open(self.deviceFile, 'r')
                lines = f.readlines()
                f.close()
                return lines
            except Exception as e:
                return False
        else:
            return False

    def read(self):
        attempts = 0
        while attempts < self.maxAttempts:
            lines = self.readRawTemp()
            if lines:
                if lines[0].strip()[-3:] == 'YES':
                    break;
                else:
                    continue;
            attempts += 1
            time.sleep(2)
        if attempts >= self.maxAttempts:
            return "read_error"
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = float(temp_string) / 1000.0
            return round(temp, 2)
        else:
            return "read_error"
