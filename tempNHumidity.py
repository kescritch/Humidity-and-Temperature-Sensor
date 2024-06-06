import time
from board import *
from pandas import DataFrame
from adafruit_bus_device.i2c_device import I2CDevice


#use $env:BLINKA_FT232H=1 for env

ADDRESS = 0x44
TOBJ = 0xE0

# creating I2C
i2c = I2C()
i2c_dev = I2CDevice(i2c, ADDRESS)
outBuff = bytearray(2)
inBuff = bytearray(5) #2 bites for temp, 1 bite checksum, and 2 bites humidity

check = False

#vars for data frame
sec = 0
secDF = []
tempData = []
humidityData = []

#set delay in sec
delay = .5

def tempNHumidity(outBuff,inBuff): #Getting object temperature 

  outBuff[0] = (0x24)
  
  i2c_dev.write_then_readinto(outBuff, inBuff, out_end=None)
  return temp_c(inBuff),humidity(inBuff)

def temp_c(data): #Converting bits 0 and 1 to C 
  msb = data[0]
  lsb = data[1]

  value = (msb << 8) | lsb
  temp = (-45+175*((value)/((2**16)-1)))

  return round(temp,2)

def humidity(data): #Converting bits 3 and 4 to %RH
  msb = data[3]
  lsb = data[4]

  value = (msb << 8) | lsb
  humidity = ((value/(2**16-1)) * 100)

  return round(humidity,2)

def runner(): #Returns the temps as a string
    data = tempNHumidity(outBuff,inBuff)
    tempData.append(data[0])
    humidityData.append(data[1])
    print (data)




while(True):
  df = DataFrame ({"Time (s)" : secDF,"Temperature (c)" : tempData, "Humidity (%RH)" : humidityData})
  df.to_excel('test.xlsx')

  runner()

  time.sleep(delay)
  
  secDF.append(sec)  
  sec+=delay


  
     

