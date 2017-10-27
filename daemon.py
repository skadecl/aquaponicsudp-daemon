import time
from modules.dispatcher import Dispatcher
from modules.datafactory import DataFactory

from modules.sensors.analog import AnalogSensor
from modules.sensors.dht22 import DHT22Sensor
from modules.sensors.ds18b20 import DS18B20Sensor
from modules.sensors.fake import FakeSensor

#Main MSG
print "#### AquaponicsUDP Daemon RPi ####"
print "####      Roberto Roman       ####"

#CONFIG
verbose = True #Prints messages (INFO)
logErrors = True #Prints errors
apiUrl = 'http://localhost:1337/push' #API URL to make POST requests
maxDispatchAttempts = 10
measureFrequency = 3 #Measure freq in seconds

#MainLoop
def daemonLoop():
    #Create Dispatcher and DataFactory
    dispatcher = Dispatcher(apiUrl, verbose, logErrors, maxDispatchAttempts)
    dataFactory = DataFactory(verbose, logErrors)

    #Create Sensors
    # fakeTempSensor = FakeSensor(1, "Fake temperature sensor", 25, 27)
    # fakeLuxSensor = FakeSensor(2, "Fake lux sensor", 400, 650)
    # fakeHumSensor = FakeSensor(3, "Fake humidity sensor", 55, 57)
    dht22Sensor = DHT22Sensor(4, "DHT22 Temperature", "temperature", 22)
    ds18b20Sensor = DS18B20Sensor(5, "DS18B20 Temperature", 15)


    #Subscribe sensors to DataFactory
    # dataFactory.subscribe(fakeTempSensor)
    # dataFactory.subscribe(fakeLuxSensor)
    # dataFactory.subscribe(fakeHumSensor)
    dataFactory.subscribe(dht22Sensor)
    dataFactory.subscribe(ds18b20Sensor)

    #Actual Loop
    while True:
        dispatcher.addSet(dataFactory.getData())
        time.sleep(measureFrequency)

#Main Sentinel
if __name__ == "__main__":
    daemonLoop()
