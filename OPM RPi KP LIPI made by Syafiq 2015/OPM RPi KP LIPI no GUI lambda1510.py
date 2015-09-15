import spidev
from time import sleep
import os
from math import log
import RPi.GPIO as gpio

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 2000000
gpio.setmode(gpio.BCM)
gpio.setup((5,6,20,13,19), gpio.OUT)
gpio.output((19,13,6,5,20), True)
y=1
array=[]

def read(channel):
    if (channel < 0) | (channel > 1):
        return -1
    adc = spi.xfer2([6,(channel)<<6,0])
    data = ((adc[1]&15)<<8) + adc[2]
    return data

def konversi(data):
    volt = (data*5)/float(4095)
    volt = round(volt, 3)
    return volt
  
while True :
    adcv = read(0)
    konv = konversi(adcv)
    if (0.5>konv)&(y==1):
        gpio.output(19, False)
        print('Device Mode 2')
        y=2
    else:
        if (0.5>konv)&(y==2):
            gpio.output(13, False)
            print('Device Mode 3')
            y=3
        else :
            if (0.5>konv)&(y==3):
                gpio.output(6, False)
                print('Device Mode 4')
                y=4
            else:
                if (0.5>konv)&(y==4):
                    gpio.output(5, False)
                    print('Device Mode 5')
                    y=5
                else:
                    if (0.5>konv):
                        print('Device Outrange')

    if (konv>4.9)&(y==2):
        gpio.output(19, True)
        print('Device Mode 1')
        y=1
    else:
        if (konv>4.9)&(y==3):
            gpio.output(13, True)
            print('Device Mode 2')
            y=2
        else :
            if (konv>4.9)&(y==4):
                gpio.output(6, True)
                print('Device Mode 3')
                y=3
            else:
                if (konv>4.9)&(y==5):
                    gpio.output(5, True)
                    print('Device Mode 4')
                    y=4
                else:
                    if (konv>4):
                        print('Device Outrange') 
    
    sleep(2)
    adcv = read(0)
    konv = konversi(adcv)
    if y==5 :
        x = (log((konv/14825)))/0.224
        x = round(x, 2)
        print ("Desibel: ", x)
    elif y==4 :
        x = (log((konv/1745)))/0.230
        x = round(x, 2)
        print ("Desibel: ", x)
    elif y==3 :
        x = (log((konv/176.1)))/0.231
        x = round(x, 2)
        print ("Desibel: ", x)
    elif y==2 :
        x = (log((konv/16.83)))/0.229
        x = round(x, 2)
        print ("Desibel: ", x)
    elif y==1 :
        x = (log((konv/1.638)))/0.225
        x = round(x, 2)
        print ("Desibel: ", x)
        
    print("Volt Result : ", konv)
    array.append(x)
    
