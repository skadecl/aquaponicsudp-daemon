# Dispatcher lib
# Roberto Roman

import requests
import datetime
from measurement import Measurement
from measurement import MeasurementLoad
from logger import AQLog

class Dispatcher:
    queue = None
    apiUrl = None
    verbose = None
    logErrors = None
    maxAttempts = None

    def __init__(self, pApiUrl, pVerbose, pLogErrors, pMaxAttempts):
        self.queue = []
        self.apiUrl = pApiUrl
        self.verbose = pVerbose
        self.logErrors = pLogErrors
        self.maxAttempts = pMaxAttempts

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

    def dispatch(self):
        if len(self.queue) == 0:
            if self.verbose:
                AQLog("INFO", "Nothing to dispatch")
            return

        #Dispatching process
        for load in self.queue:
            if len(load.measurements) == 0 and len(load.errors) == 0:
                self.queue.remove(load)
                if self.verbose:
                    AQLog("INFO", "Discarded empty MeasurementLoad")
            elif load.attempts >= self.maxAttempts:
                self.queue.remove(load)
                if self.verbose:
                    AQLog("INFO", "Discarded MeasurementLoad", "Too many attempts")
            else:
                try:
                    r = requests.post(self.apiUrl, data=load.toJSON())
                    if r.status_code == 201:
                        self.queue.remove(load)
                        if self.verbose:
                            AQLog("INFO", "MeasurementLoad sent")
                    else:
                        load.attempts += 1
                        if self.logErrors:
                            AQLog("ERROR", "MeasurementLoad could not be sent", "HTTP " + r.status_code)
                except Exception as e:
                    load.attempts += 1
                    if self.logErrors:
                        AQLog("ERROR", "Load could not be sent", "Network Error")
