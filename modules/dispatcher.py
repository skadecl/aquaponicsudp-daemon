# Dispatcher lib
# Roberto Roman

import requests
import datetime
import json
from measurement import Measurement
from measurement import MeasurementLoad
from actionParser import parseActionsFromJSON
from logger import AQLog

class Dispatcher:
    queue = None
    apiUrl = None
    verbose = None
    logErrors = None
    maxAttempts = None
    actions = None

    def __init__(self, pApiUrl, pVerbose, pLogErrors, pMaxAttempts):
        self.queue = []
        self.apiUrl = pApiUrl
        self.verbose = pVerbose
        self.logErrors = pLogErrors
        self.maxAttempts = pMaxAttempts
        self.actions = []

        if self.verbose:
            AQLog("INFO", "Dispatcher init OK")

    def addSet(self, thisSet):
        if isinstance(thisSet, MeasurementLoad):
            self.queue.append(thisSet)
            if self.verbose:
                AQLog("INFO", "MeasurementLoad added to dispatcher")
        else:
            if self.logErrors:
                AQLog("ERROR", "MeasurementLoad could not be added")

        self.dispatch()

    def updateActions(self, actions):
        try:
            r = requests.post(self.apiUrl + 'actions', json=actions)
            if self.verbose:
                AQLog("INFO", "Trying to update actions status")
            if r.status_code == 200:
                if self.verbose:
                    AQLog("INFO", str(len(actions)) + " actions updated")
            else:
                if self.logErrors:
                    AQLog("ERROR", "Actions update could not be sent", "HTTP " + r.status_code)
        except Exception as e:
            if self.logErrors:
                AQLog("ERROR", "Actions update could not be sent", "Network Error")

    def hasActions(self):
        return len(self.actions) > 0

    def dispatch(self):
        if len(self.queue) == 0:
            if self.verbose:
                AQLog("INFO", "Nothing to dispatch")
            return

        #Dispatching process
        newQueue = []
        for load in self.queue:
            if len(load.measurements) == 0 and len(load.errors) == 0:
                continue
                if self.verbose:
                    AQLog("INFO", "Discarded empty MeasurementLoad")
            elif load.attempts >= self.maxAttempts:
                continue
                if self.verbose:
                    AQLog("INFO", "Discarded MeasurementLoad", "Too many attempts")
            else:
                try:
                    r = requests.post(self.apiUrl + 'push', data=load.toJSON())
                    if self.verbose:
                        AQLog("INFO", "Trying to send load")
                    if r.status_code == 201 or r.status_code == 210:
                        if self.verbose:
                            AQLog("INFO", "MeasurementLoad sent OK")
                        if r.status_code == 210:
                            self.actions += parseActionsFromJSON(r.content)
                    else:
                        load.attempts += 1
                        newQueue.append(load)
                        if self.logErrors:
                            AQLog("ERROR", "MeasurementLoad could not be sent", "HTTP " + r.status_code)
                except Exception as e:
                    load.attempts += 1
                    newQueue.append(load)
                    if self.logErrors:
                        AQLog("ERROR", "Load could not be sent", "Network Error")
        self.queue = newQueue
