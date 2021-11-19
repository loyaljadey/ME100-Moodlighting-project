##This is the code for the test of how lights work and will be used in the future to program different lighting schemes chosen by the user
##reference and inspiration off of https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/

##author: Michael Jia 
#         Mechanical Engineering 2024

##IMPORTS##
import machine
##must import neopixel in python via
##run the following command in the terminal
##windows: pip install adafruit-circuitpython-neopixel
##linux: sudo pip install adafruit-circuitpython-neopixel
import neopixel
import math
import time

#physical constraints: 
#   the leds are space 13mm between each other
#   the gravity is 9.8 m/s^2
LED_distance = 0.013
gravity = 9.8
#setting the led count on the device
LED_count = 300
#setting the gpio pin used as PWM to the lights
pin = 27

#creating a neopixel object to use the PWM signal to power the lights
pixels = neopixel.NeoPixel(machine.Pin(pin), LED_count)

##method for clearing all the leds
# param: none
# type: none
# output: none 
# type: none
def clear():
    for i in range(LED_count):
        print("clearing")
        pixels[i] = (0,0,0)
        pixels.write()
        #time.sleep(0.5)
    print("cleared")

##method for making a continuous strip of lights
# param: none
# type: none
# output: none 
# type: none
def continuousStrip():
    for i in range(LED_count):
        print("strip")
        pixels[i] = (255,0,0)
        pixels.write()
        time.sleep(0.5)

##helper method for doing the rain time intervals
# param: length
# type: none
# output: []
# type: int
# math and physics calculations can be found on raincalc.txt
def rainHelper(length):
    #d = 0.5*g*t^2
    #generates the distances of the leds from the start (start is y = 0 meters)
    d = []
    for i in range(length+1):
        d.append(LED_distance*i)

    print(len(d))
    
    #generates the times for the particle to travel the distances
    t = []
    divisor = 0.5*gravity
    for i in [x/divisor for x in d]:
        t.append(math.sqrt(i))

    print(len(t))

    #generates the time intervals for the particle to travel in between the leds
    deltaT = []
    for i in range(len(t)-1):
        deltaT.append(t[i+1]-t[i])

    print(len(deltaT))

    return deltaT


##method for doing the rain animation of a water drop dropping down
# math and physics calculations can be found on raincalc.txt
# param: start, end, timeofday
# type: int, int, string
# output: none
# type: none
# start is the start number of the led
# end is the end number of the led
# timeofday tells what time of the day it is
def rainyDay(start, end, timeofday, speed):
    timeInterval = rainHelper(end-start)
    if(speed == "slow" or speed == "Slow"):
        if(timeofday == "day" or timeofday == "Day"):
            for i in range(start, end):
                #blue light for the rain drop
                pixels[i] = (0,0,255)
                pixels.write()
                time.sleep(timeInterval[i]*20)
                pixels[i] = (0,0,0)
                pixels.write()
        else:
            for i in range(start, end):
                #blue light for the rain drop
                pixels[i] = (0,0,255)
                pixels.write()
                time.sleep(timeInterval[i]*20)
                pixels[i] = (0,0,0)
                pixels.write()
    else:
        if(timeofday == "day" or timeofday == "Day"):
            for i in range(start, end):
                #blue light for the rain drop
                pixels[i] = (0,0,255)
                pixels.write()
                time.sleep(timeInterval[i])
                pixels[i] = (0,0,0)
                pixels.write()
        else:
            for i in range(start, end):
                #blue light for the rain drop
                pixels[i] = (0,0,255)
                pixels.write()
                time.sleep(timeInterval[i])
                pixels[i] = (0,0,0)
                pixels.write()

##method for have all the colors on 
# param: none
# type: none
# output: none 
# type: none
# reference for range method in the for loop https://www.w3schools.com/python/ref_func_range.asp
def showAllColors():
    for i in range(0,LED_count,3):
        print("showing")
        pixels[i] = (255, 0, 0)
        pixels.write()
        time.sleep(0.5)
        pixels[i+1] = (0, 255, 0)
        pixels.write()
        time.sleep(0.5)
        pixels[i+2] = (0, 0, 255)
        pixels.write()
        time.sleep(0.5)
        

##main method
# param: none
# type: none
# output: none 
# type: none
def main():
    #clear()
    # continuousStrip()
    # clear()
    #showAllColors()
    #rainHelper(LED_count)
    rainyDay(0,50,"day","slow")

if __name__ == "__main__":
    main()
