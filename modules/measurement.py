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
    sensor = None
    message = None
    sampledate = None

    def __init__(self, pSensor, pMessage):
        self.sensor = pSensor
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
        if isinstance(sample, MeasurementError):
            self.errors.append(error)
            return True
        else:
            return False

    def toJSON(self):
        dataJson = json.dumps([ob.__dict__ for ob in self.measurements])
        errorsJson = json.dumps([ob.__dict__ for ob in self.errors])
        template = '{"measurements": %s, "errors": %s}' % (dataJson, errorsJson)
        return template
