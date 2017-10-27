# Digital Actuator
# Roberto Roman

import RPi.GPIO as gpio

class DigitalActuator:
    id = None
    name = None
    pin = None
    status = None

    def __init__(self, pId, pName, pPin, pStatus = False):
        self.id = pId
        self.name = pName
        self.pin = pPin
        self.status = pStatus
        self.setStatus(self.status)
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin, gpio.OUT)

    def setStatus(self, status):
        self.status = status
        gpio.output(self.pin, status)
