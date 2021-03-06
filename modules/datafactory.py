# Data Factory lib
# Roberto Roman

import sys
from logger import AQLog
from measurement import Measurement
from measurement import MeasurementError
from measurement import MeasurementLoad

#DataFactory
class DataFactory:
    sensors = None
    verbose = None
    logErrors = None

    def __init__(self, pVerbose, pLogErrors):
        self.sensors = []
        self.verbose = pVerbose
        self.logErrors = pLogErrors
        if self.verbose:
            AQLog("INFO", "DataFactory init OK")

    def subscribe(self, sensor):
        if hasattr(sensor, 'read') == False:
            if self.logErrors:
                sys.exit("[FATAL ERROR] " + sensor.__class__.__name__ + " class does not have a read() method")
        if hasattr(sensor, 'id') == False:
            if self.logErrors:
                sys.exit("[FATAL ERROR] " + sensor.__class__.__name__ + " class does not have an id attribute")
        if hasattr(sensor, 'name') == False:
            if self.logErrors:
                sys.exit("[FATAL ERROR] " + sensor.__class__.__name__ + " class does not have a name attribute")
        else:
            self.sensors.append(sensor)
            if self.verbose:
                AQLog("INFO", "Sensor added to DataFactory", sensor.name)

    def getData(self):
        thisLoad = MeasurementLoad()
        for sensor in self.sensors:
            if self.verbose:
                AQLog("INFO", "Trying to read", sensor.name)
            thisSample = sensor.read()
            if thisSample != "read_error":
                thisMeasurement = Measurement(sensor.id, thisSample)
                if thisLoad.addSample(thisMeasurement):
                    if self.verbose:
                        AQLog("INFO", "Sample added to MeasurementLoad", sensor.name)
                else:
                    errorMsg = "Error adding sample to MeasurementLoad"
                    thisLoad.addError(MeasurementError(sensor.id, errorMsg))
                    if self.logErrors:
                        AQLog("ERROR", errorMsg, sensor.name)
            else:
                errorMsg = "No se pudo leer el sensor"
                thisLoad.addError(MeasurementError(sensor.id, 1, errorMsg))
                if self.logErrors:
                    AQLog("ERROR", errorMsg, sensor.name)
        return thisLoad
