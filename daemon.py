import time
from modules.dispatcher import Dispatcher
from modules.datafactory import DataFactory
from modules.actuatorHandler import ActuatorHandler

from modules.sensors.analog import AnalogSensor
from modules.sensors.dht22 import DHT22Sensor
from modules.sensors.ds18b20 import DS18B20Sensor
from modules.sensors.fake import FakeSensor

from modules.actuators.fakeActuator import FakeActuator
from modules.actuators.digitalActuator import DigitalActuator

#Main MSG
print "#### AquaponicsUDP Daemon RPi ####"
print "####      Roberto Roman       ####"

#CONFIG
verbose = True #Prints messages (INFO)
logErrors = True #Prints errors
apiUrl = 'http://192.168.0.10:1337/spu/' #API URL to make POST requests
spuToken = 'Replace this with your own token' #Invalid tokens will cause 403HTTP Error
requestTimeout = 10
maxDispatchAttempts = 10
measureFrequency = 10 #Measure freq in seconds
heartbeatFrequency = 3 #Heartbeat freq in seconds

#MainLoop
def daemonLoop():
    #Init Handlers
    dispatcher = Dispatcher(apiUrl, spuToken, requestTimeout, verbose, logErrors, maxDispatchAttempts)
    dataFactory = DataFactory(verbose, logErrors)
    actuatorHandler = ActuatorHandler(verbose, logErrors)

    #Init Sensors
    # dataFactory.subscribe( FakeSensor(1, "Fake temperature sensor", 25, 27) )
    # dataFactory.subscribe( FakeSensor(2, "Fake lux sensor", 400, 650) )
    # dataFactory.subscribe( FakeSensor(3, "Fake humidity sensor", 55, 57) )
    dataFactory.subscribe( DHT22Sensor(1, "DHT22 Temperature", "temperature", 22) )
    dataFactory.subscribe( DS18B20Sensor(2, "DS18B20 Temperature", 15) )
    dataFactory.subscribe( AnalogSensor(3, "Potentiometer 1", 1, 1, 1) )
    dataFactory.subscribe( AnalogSensor(4, "UV Sensor", 2, 1, 0.00496) )
    dataFactory.subscribe( DHT22Sensor(5, "DHT22 Humidity", "humidity", 22) )

    #Init Actuators
    actuatorHandler.subscribe( DigitalActuator(1, "Relay slot 1", 16, False) )
    actuatorHandler.subscribe( FakeActuator(2, "Fake relay 2", False) )


    #Control time
    lastDispatch = 0

    #Actual Loop
    while True:
        #Heartbeat
        dispatcher.sendHeartbeat(actuatorHandler.getActuatorsJSON())
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
