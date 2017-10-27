from logger import AQLog
import json

class ActuatorHandler:
    actuators = None
    actionsQueue = None
    toUpdate = None
    logErrors = None
    verbose = None

    def __init__(self, pVerbose, pLogErrors):
        self.actuators = []
        self.actionsQueue = []
        self.toUpdate = []
        self.verbose = pVerbose
        self.logErrors = pLogErrors

    def subscribe(self, actuator):
        if hasattr(actuator, 'id') == False:
            if self.logErrors:
                sys.exit("[FATAL ERROR] " + actuator.__class__.__name__ + " class does not have an id attribute")
        if hasattr(actuator, 'name') == False:
            if self.logErrors:
                sys.exit("[FATAL ERROR] " + actuator.__class__.__name__ + " class does not have a name attribute")
        else:
            self.actuators.append(actuator)
            if self.verbose:
                AQLog("INFO", "Actuator added to Handler", actuator.name)

    def addActions(self, pActions):
        # TODO: Validate actions
        self.actionsQueue += pActions
        self.performActions()

    def performActions(self):
        while self.actionsQueue:
            action = self.actionsQueue[0]
            for actuator in self.actuators:
                if action.actuator == actuator.id:
                    actuator.setStatus(action.status)
                    self.toUpdate.append(action.id)
                    self.actionsQueue.pop(0)
                    if self.verbose:
                        AQLog("INFO", "Actuator status changed to " + str(actuator.status), actuator.name)
                    break
        if len(self.actionsQueue) > 0:
            if self.verbose:
                AQLog("INFO", "Discarded " + str(len(self.actionsQueue)) + " actions", "No matching actuators")
            self.actionsQueue = []

    def hasUpdates(self):
        return len(self.toUpdate) > 0
