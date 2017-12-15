import time
from modules.dispatcher import Dispatcher
from modules.datafactory import DataFactory
from modules.actuatorHandler import ActuatorHandler

from modules.sensors.analog import AnalogSensor
from modules.sensors.dht22 import DHT22Sensor
from modules.sensors.ds18b20 import DS18B20Sensor
from modules.sensors.switch import SwitchSensor
from modules.sensors.fake import FakeSensor

from modules.actuators.fakeActuator import FakeActuator
from modules.actuators.digitalActuator import DigitalActuator

#Main MSG
print "#### AquaponicsUDP Daemon RPi ####"
print "####      Roberto Roman       ####"

#CONFIG
verbose = True #Prints messages (INFO)
logErrors = True #Prints errors
apiUrl = 'http://acuaiot.com/api/spu/' #API URL to make POST requests
spuToken = 'f9907db9ee752a989e850cb735b48bedcd4dd6333bc978e1503b9430b40cece4' #Invalid tokens will cause 403HTTP Error
requestTimeout = 10
maxDispatchAttempts = 10
measureFrequency = 300 #Measure freq in seconds
heartbeatFrequency = 30 #Heartbeat freq in seconds

#MainLoop
def daemonLoop():
    #Init Handlers
    dispatcher = Dispatcher(apiUrl, spuToken, requestTimeout, verbose, logErrors, maxDispatchAttempts)
    dataFactory = DataFactory(verbose, logErrors)
    actuatorHandler = ActuatorHandler(verbose, logErrors)

    #Init Sensors
    dataFactory.subscribe( DHT22Sensor(1, "DHT22 Temperature", "temperature", 21) )
    dataFactory.subscribe( DS18B20Sensor(2, "DS18B20 Temperature", 15) )
    dataFactory.subscribe( DHT22Sensor(3, "DHT22 Humidity", "humidity", 21) )
    dataFactory.subscribe( AnalogSensor(4, "pH Sensor", 0, 1, 3.5) )
    dataFactory.subscribe( AnalogSensor(5, "UV Sensor", 1, 1, 1.535) )
    dataFactory.subscribe( AnalogSensor(6, "Illumination", 1, 1, 307) )
    dataFactory.subscribe( SwitchSensor(7, "Fishtank Level", 13) )
    dataFactory.subscribe( SwitchSensor(8, "Tank Level", 20) )

    #Init Actuators
    actuatorHandler.subscribe( DigitalActuator(1, "Relay slot 1", 16, False) )
    actuatorHandler.subscribe( DigitalActuator(2, "Relay slot 2", 26, False) )


    #Control time
    lastDispatch = 0

    #Actual Loop
    while True:
        #Heartbeat
        dispatcher.sendHeartbeat(actuatorHandler.getActuatorsJSON())
        actuatorHandler.addActions(dispatcher.getActions())
        dispatcher.confirmActions(actuatorHandler.getUpdates())


        #Dispatch data (Measure)
        now = time.time()
        if (now - lastDispatch) > measureFrequency:
            dispatcher.addSet(dataFactory.getData())
            actuatorHandler.addActions(dispatcher.getActions())
            dispatcher.confirmActions(actuatorHandler.getUpdates())
            lastDispatch = time.time()

        #Sleep until next heartbeat
        time.sleep(heartbeatFrequency)

#Main Sentinel
if __name__ == "__main__":
    daemonLoop()
