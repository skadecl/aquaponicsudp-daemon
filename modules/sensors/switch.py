#SwitchSensor lib
#Roberto Roman

import time
import RPi.GPIO as GPIO

class SwitchSensor:
    id = None
    name = None
    pin = None

    def __init__(self, pId, pName, pPin):
        self.id = pId
        self.name = pName
        self.pin = pPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read(self):
        try:
            state = GPIO.input(self.pin)
            return state
        except Exception as e:
            return "read_error"
