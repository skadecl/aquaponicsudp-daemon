# ActionParser
# Roberto Roman

# This class is constructed from a JSON object.
import json

class Action:
    id = None
    actuator = None
    value = None

    def __init__(self, jsonDict):
        self.__dict__ = jsonDict

def parseActionsFromJSON(jsonString):
    dictArray = json.loads(jsonString)
    actions = []
    for actionDict in dictArray:
        actions.append(Action(actionDict))
    return actions
