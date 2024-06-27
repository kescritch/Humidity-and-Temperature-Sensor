import os
import time

from pandas import DataFrame
os.environ["BLINKA_FT232H"] = "1"
from board import I2C
from adafruit_bus_device.i2c_device import I2CDevice


THRESHOLD = 0.008
delay = 1
"""
address for the 
"""
class TemperatureReadout:
  def __init__(self, address):
    i2c = I2C()
    self.dev = I2CDevice(i2c, address)

  """
    Gets the temperature and humidity from sensor returns temp and humidity as a tuple. [0] = temp [1] = humidity
  """
  def getTemperatureHumidity(self):
    message = bytearray(2)
    result = bytearray(5)
    message[0] = (0x24)

    self.dev.write_then_readinto(message, result, out_end=None)

    return self._temp_c(result), self._humidity(result)

  """
  converts the data into c
  """
  def _temp_c(self, data: bytearray) -> float: #Converting bits 0 and 1 to C 
    msb = data[0]
    lsb = data[1]

    value = (msb << 8) | lsb
    temp = (-45+175*((value)/((2**16)-1)))

    return round(temp,2)
  """
  converts the data %RH
  """
  def _humidity(self, data: bytearray) -> float: #Converting bits 3 and 4 to %RH
    msb = data[3]
    lsb = data[4]

    value = (msb << 8) | lsb
    humidity = ((value/(2**16-1)) * 100)

    return round(humidity,2)

def main(): 
  try:
    while(True):

      mcu = TemperatureReadout(0x44)

      temp = mcu.getTemperatureHumidity()[0]
      humidity = mcu.getTemperatureHumidity()[1]

  finally:
      df = {"Temperature" : temp, "Humidity" : humidity}
      df = DataFrame(df)
      df.to_csv("results.csv")

      print(f"Temperature: {temp} Humidity: {humidity}")

if __name__ == "__main__":
  main()