import time
from modules.dispatcher import Dispatcher
from modules.datafactory import DataFactory

from modules.sensors.analog import AnalogSensor
from modules.sensors.dht22 import DHT22Sensor
from modules.sensors.fake import FakeSensor

#Main MSG
print "#### AquaponicsUDP Daemon RPi ####"
print "####      Roberto Roman       ####"

#CONFIG
verbose = True #Prints messages (INFO)
logErrors = True #Prints errors
apiUrl = 'http://192.168.0.6:1337/push' #API URL to make POST requests
measureFrequency = 60 #Measure freq in seconds

#MainLoop
def daemonLoop():
    #Create Dispatcher and DataFactory
    dispatcher = Dispatcher(apiUrl, verbose, logErrors)
    dataFactory = DataFactory(verbose, logErrors)

    #Create Sensors
    fakeTempSensor = FakeSensor(1, "Fake temperature sensor", 25, 27)
    fakeLuxSensor = FakeSensor(2, "Fake lux sensor", 400, 650)
    fakeHumSensor = FakeSensor(3, "Fake humidity sensor", 55, 57)


    #Subscribe sensors to DataFactory
    dataFactory.subscribe(fakeTempSensor)
    dataFactory.subscribe(fakeLuxSensor)
    dataFactory.subscribe(fakeHumSensor)

    #Actual Loop
    while True:
        dispatcher.addSet(dataFactory.getData())
        time.sleep(measureFrequency)

#Main Sentinel
if __name__ == "__main__":
    daemonLoop()
