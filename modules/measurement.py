# Measurement lib
# Roberto Roman

import datetime
import json

# Measurement Class
class Measurement:
    sensor = None
    value = None
    sampledate = None

    def __init__(self, pSensor, pValue):
        self.sensor = pSensor
        self.value = pValue
        self.sampledate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# MeasurementError Class
class MeasurementError:
    device = None
    type = None
    message = None
    sampledate = None

    def __init__(self, pDevice, pType, pMessage):
        self.device = pDevice
        self.type = pType
        self.message = pMessage
        self.sampledate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Measurement Load Class
class MeasurementLoad:
    measurements = None
    errors = None
    attempts = None

    def __init__(self):
        self.measurements = []
        self.errors = []
        self.attempts = 0

    def hasErrors(self):
        return len(self.errors) != 0

    def addSample(self, sample):
        if isinstance(sample, Measurement):
            self.measurements.append(sample)
            return True
        else:
            return False

    def addError(self, error):
        if isinstance(error, MeasurementError):
            self.errors.append(error)
            return True
        else:
            return False

    def toJSON(self):
        dataJson = json.dumps([ob.__dict__ for ob in self.measurements])
        errorsJson = json.dumps([ob.__dict__ for ob in self.errors])
        isFresh = ('true' if self.attempts == 0 else 'false')
        template = '{"measurements": %s, "errors": %s, "fresh": %s}' % (dataJson, errorsJson, isFresh)
        return template
