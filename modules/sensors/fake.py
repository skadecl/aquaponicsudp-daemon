# FakeSensor
# Roberto Roman

import random

class FakeSensor:
    id = None
    name = None
    minValue = None
    maxValue = None

    def __init__(self, pId, pName, pMinValue, pMaxValue, pWithError = False):
        self.id = pId
        self.name = pName
        self.minValue = pMinValue
        self.maxValue = pMaxValue
        self.withError = pWithError

    def read(self):
        if self.withError:
            return False
        else:
            return round(random.uniform(self.minValue, self.maxValue), 2)
