# DHT22Sensor
# Roberto Roman
import Adafruit_DHT
import time

class DHT22Sensor:
    id = None
    name = None
    type = None
    pin = None
    sensor = None

    def __init__(self, pId, pName, pType, pPin):
        self.id = pId
        self.name = pName
        self.type = pType
        self.pin = pPin
        self.sensor = Adafruit_DHT.DHT22

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

        if humidity is not None and temperature is not None:
            if self.type == 'temperature':
                return round(temperature, 2)
            if self.type == 'humidity':
                return round(humidity, 2)
        else:
            return "read_error"
