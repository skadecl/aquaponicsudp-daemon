# DHT22Sensor
# Roberto Roman

class DHT22Sensor:
    id = None
    name = None
    type = None
    pin = None

    def __init__(self, pId, pName, pType, pPin):
        self.id = pId
        self.name = pName
        self.type = pType
        self.pin = pPin

    def read(self):
        # TODO: Handle get data from Raspberry
        return False
