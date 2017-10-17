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

# Measurement Load Class
class MeasurementLoad:
    measurements = None
    attempts = None

    def __init__(self):
        self.measurements = []
        self.attempts = 0

    def addSample(self, sample):
        if isinstance(sample, Measurement):
            self.measurements.append(sample)
            return True
        else:
            return False

    def toJSON(self):
        return json.dumps([ob.__dict__ for ob in self.measurements])
