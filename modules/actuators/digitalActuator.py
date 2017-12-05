# Digital Actuator
# Roberto Roman

import RPi.GPIO as gpio

class DigitalActuator:
    id = None
    name = None
    pin = None
    status = None
    reverse = None

    def __init__(self, pId, pName, pPin, pStatus = False):
        self.id = pId
        self.name = pName
        self.pin = pPin
        self.status = pStatus
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin, gpio.OUT)
        self.setStatus(self.status)

    def setStatus(self, status):
        self.status = status
        gpio.output(self.pin, status)
