#AnalogSensor lib
#Roberto Roman

class AnalogSensor:
    id = None
    name = None
    mcpChannel = None

    def __init__(self, pId, pName, pChannel):
        self.id = pId
        self.name = pName
        self.mcpChannel = pChannel

    def read(self):
        # TODO: Handle get data from Raspberry
        return False
