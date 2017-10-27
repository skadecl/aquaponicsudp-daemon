# Digital Actuator
# Roberto Roman


class FakeActuator:
    id = None
    name = None
    status = None

    def __init__(self, pId, pName, pStatus = False):
        self.id = pId
        self.name = pName
        self.status = pStatus
        self.setStatus(self.status)

    def setStatus(self, status):
        self.status = status
