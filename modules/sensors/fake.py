# FakeSensor
# Roberto Roman

import random

class FakeSensor:
    id = None
    name = None
    minValue = None
    maxValue = None

    def __init__(self, pId, pName, pMinValue, pMaxValue):
        self.id = pId
        self.name = pName
        self.minValue = pMinValue
        self.maxValue = pMaxValue

    def read(self):
        return round(random.uniform(self.minValue, self.maxValue), 2)
