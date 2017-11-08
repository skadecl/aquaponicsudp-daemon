#AnalogSensor lib
#Roberto Roman

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

SPI_PORT   = 0
SPI_DEVICE = 0

class AnalogSensor:
    id = None
    name = None
    channel = None
    samples = None
    convertion = None
    mcp = None

    def __init__(self, pId, pName, pChannel, pSamples, pConvertion):
        self.id = pId
        self.name = pName
        self.channel = pChannel
        self.samples = pSamples
        self.convertion = pConvertion
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    def read(self):
        try:
            value = round(float(self.mcp.read_adc(self.channel)) * float(self.convertion), 2)
            if value == 0.0:
                value = 0.1
            return value
        except Exception as e:
            return False
