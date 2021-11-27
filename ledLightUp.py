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


##INSTANCE VARIABLES##
#physical constraints: 
#   the leds are space 13mm between each other
#   the gravity is 9.8 m/s^2
LED_distance = 0.013
gravity = 9.8
#setting the led count on the device
#the system uses 83 leds
LED_count = 83
#setting the gpio pin used as PWM to the lights
pin = 27
#colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DIMMER_BLUE = (0,0,200)
NO_COLOR = (0,0,0)
WHITE = (255,255,255)
DIMMER_WHITE = (180,180,180)
DIMMER_WHITE2 = (120,120,120)
DIMMER_WHITE3 = (10,10,10)
DIMMER_WHITE4 = (5,5,5)
ORANGE_RED = (255,70,0)

#for later use when in the assembly, we know where each led is exactly going to be
#we can replace the start and end with the exact places of the pixels
sun_pixels = [0,1,2,3,4,5,6,7]
cloud_pixels = [8,9,10,11,12,13,14,15,18,21,28,32,35,40,48,51,56,59,64,65,70,73,74,75,76,77,78,79,80,81,82,83]
rain_pixels =[16,17,19,20,22,23,24,25,26,27,29,30,31,33,34,26,37,38,39,41,42,43,44,45,46,47,49,50,52,53,54,55,57,58,60,61,62,63,66,67,68,69,71,72] 

#creating a neopixel object to use the PWM signal to power the lights
pixels = neopixel.NeoPixel(machine.Pin(pin), LED_count)


##FUNCTIONS/METHODS##
##method for clearing all the leds
# param: none
# type: none
# output: none 
# type: none
def clear():
    for i in range(LED_count):
        print("clearing")
        pixels.__setitem__(i, NO_COLOR)
        pixels.write()
        #time.sleep(0.05)
    print("cleared")

##method for have all the colors on 
# param: none
# type: none
# output: none 
# type: none
# reference for range method in the for loop https://www.w3schools.com/python/ref_func_range.asp
def showAllColors():
    for i in range(0,LED_count,3):
        print("showing")
        pixels.__setitem__(i, RED)
        pixels.write()
        time.sleep(0.125)
        pixels.__setitem__(i+1, GREEN)
        pixels.write()
        time.sleep(0.125)
        pixels.__setitem__(i+2, BLUE)
        pixels.write()
        time.sleep(0.125)

##method for making a continuous strip of lights
# param: none
# type: none
# output: none 
# type: none
def continuousStrip():
    for i in range(LED_count):
        pixels.__setitem__(i, BLUE)
        pixels.write()
        pixels.__setitem__(i,NO_COLOR)
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

##generic method for doing the rain animation of a water drop dropping down
# math and physics calculations can be found on raincalc.txt
# param: start, end, timeofday, speed
# type: int, int, string, string
# output: none
# type: none
# start is the start number of the led
# end is the end number of the led
# timeofday tells what time of the day it is, if day, then blue is brighter, if night, then dimmer
# speed tell how fast the rain drop goes, if slow then 1/20 of the actual speed, if fast then actual speed
def rainyDay(start, end, timeofday, speed):
    timeInterval = rainHelper(end-start)
    while True:
        if(speed == "slow" or speed == "Slow"):
            if(timeofday == "day" or timeofday == "Day"):
                for i in range(start, end):
                    #blue light for the rain drop
                    pixels.__setitem__(i, BLUE)
                    pixels.write()
                    time.sleep(timeInterval[i]*20)
                    pixels.__setitem__(i, NO_COLOR)
                    pixels.write()
            else:
                for i in range(start, end):
                    #blue light for the rain drop
                    pixels.__setitem__(i, DIMMER_BLUE)
                    pixels.write()
                    time.sleep(timeInterval[i]*20)
                    pixels.__setitem__(i, NO_COLOR)
                    pixels.write()
        else:
            if(timeofday == "day" or timeofday == "Day"):
                for i in range(start, end):
                    #blue light for the rain drop
                    pixels.__setitem__(i, BLUE)
                    pixels.write()
                    time.sleep(timeInterval[i])
                    pixels.__setitem__(i, NO_COLOR)
                    pixels.write()
            else:
                for i in range(start, end):
                    #blue light for the rain drop
                    pixels.__setitem__(i, DIMMER_BLUE)
                    pixels.write()
                    time.sleep(timeInterval[i])
                    pixels.__setitem__(i, NO_COLOR)
                    pixels.write()

        time.sleep(1)

##specific method for doing the rain animation of a water drop dropping down
def rainyDaySpecific(timeofday, speed):
    timeInterval = rainHelper(len(rain_pixels))
    while True:
        if(speed == "slow" or speed == "Slow"):
            if(timeofday == "day" or timeofday == "Day"):
                for i in rain_pixels:
                    #blue light for the rain drop
                    pixels.__setitem__(i, BLUE)
                    pixels.write()
                    time.sleep(timeInterval[i]*20)
                    pixels.__setitem__(i, NO_COLOR)
                    pixels.write()
            else:
                for i in rain_pixels:
                    #blue light for the rain drop
                    pixels.__setitem__(i, DIMMER_BLUE)
                    pixels.write()
                    time.sleep(timeInterval[i]*20)
                    pixels.__setitem__(i, NO_COLOR)
                    pixels.write()
        else:
            if(timeofday == "day" or timeofday == "Day"):
                for i in rain_pixels:
                    #blue light for the rain drop
                    pixels.__setitem__(i, BLUE)
                    pixels.write()
                    time.sleep(timeInterval[i])
                    pixels.__setitem__(i, NO_COLOR)
                    pixels.write()
            else:
                for i in rain_pixels:
                    #blue light for the rain drop
                    pixels.__setitem__(i, DIMMER_BLUE)
                    pixels.write()
                    time.sleep(timeInterval[i])
                    pixels.__setitem__(i, NO_COLOR)
                    pixels.write()

        time.sleep(1)

##general method for doing the sun animation of the lights circling the sun then alternating the lights
# param: start, end
# type: int, int
# output: none
# type: none
# start is the start number of the led
# end is the end number of the led
def sunnyDay(start, end):
    #turn on all the lights for the sun
    for i in range(start, end):
        #orange red light for the sun
        pixels.__setitem__(i, ORANGE_RED)
        pixels.write()
        time.sleep(0.25)
    #blink odd and evens on and off
    #alternating
    odds = []
    evens = []
    for i in range(start,end):
        if(i%2 == 0):
            evens.append(i)
        else:
            odds.append(i)
    #print(odds)
    #print(evens)

    #turning light on and off alternating between odds and evens
    repeat = True
    while repeat:
        #odds
        #turn on
        for i in odds:
            #orange red light for the sun
            pixels.__setitem__(i, ORANGE_RED)
        pixels.write()
        time.sleep(0.5)
        #turn off
        for i in odds:
            pixels.__setitem__(i, NO_COLOR)
        time.sleep(0.25)

        #evens
        #turn on
        for i in evens:
            #orange red light for the sun
            pixels.__setitem__(i, ORANGE_RED)
        pixels.write()
        time.sleep(0.5)
        #turn off
        for i in evens:
            pixels.__setitem__(i, NO_COLOR)
        time.sleep(0.25)
        #repeat += 1 

##specific method for doing the sun animation of the lights circling the sun then alternating the lights
def sunnyDaySpecific():
    #turn on all the lights for the sun
    for i in sun_pixels:
        #orange red light for the sun
        pixels.__setitem__(i, ORANGE_RED)
        pixels.write()
        time.sleep(0.25)
    #blink odd and evens on and off
    #alternating
    odds = []
    evens = []
    for i in sun_pixels:
        if(i%2 == 0):
            evens.append(i)
        else:
            odds.append(i)
    #print(odds)
    #print(evens)

    #turning light on and off alternating between odds and evens
    repeat = True
    while repeat:
        #odds
        #turn on
        for i in odds:
            #orange red light for the sun
            pixels.__setitem__(i, ORANGE_RED)
        pixels.write()
        time.sleep(0.5)
        #turn off
        for i in odds:
            pixels.__setitem__(i, NO_COLOR)
        time.sleep(0.25)

        #evens
        #turn on
        for i in evens:
            #orange red light for the sun
            pixels.__setitem__(i, ORANGE_RED)
        pixels.write()
        time.sleep(0.5)
        #turn off
        for i in evens:
            pixels.__setitem__(i, NO_COLOR)
        time.sleep(0.25)
        #repeat += 1 

##generic method for doing the cloud animation of the lights circling the cloud
# param: start, end
# type: int, int
# output: none
# type: none
# start is the start number of the led
# end is the end number of the led
whiteLED1 = [DIMMER_WHITE4,DIMMER_WHITE2,WHITE]
whiteLED2 = [WHITE,DIMMER_WHITE4,DIMMER_WHITE2]
whiteLED3 = [DIMMER_WHITE2,DIMMER_WHITE4,WHITE]
def cloudyDay(start, end):
    #turns on the different whites initally
    for i in range(start, end, 3):
        for j in range(0,3):
            #print(whiteLED[j])
            pixels.__setitem__(i+j, whiteLED1[j])
            pixels.write()
            time.sleep(0.125)
    #shift its current color down an led every 3 leds like a wave
    x = True
    while x:
        for i in range(start, end, 3):
            for j in range(0,3):
                #print(whiteLED[j])
                pixels.__setitem__(i+j, whiteLED1[j])
                pixels.write()
                time.sleep(0.125)
        time.sleep(0.5)
        for i in range(start, end, 3):
            for j in range(0,3):
                #print(whiteLED[j])
                pixels.__setitem__(i+j, whiteLED2[j])
                pixels.write()
                time.sleep(0.125)
        time.sleep(0.5)
        for i in range(start, end, 3):
            for j in range(0,3):
                #print(whiteLED[j])
                pixels.__setitem__(i+j, whiteLED3[j])
                pixels.write()
                time.sleep(0.125)
        time.sleep(0.5)
        #x+=1

##specific method for doing the cloud animation of the lights circling the cloud
def cloudyDaySpecific():
    #turns on the different whites initally
    for i in range(0, len(cloud_pixels), 3):
        for j in range(0,3):
            #print(whiteLED[j])
            pixels.__setitem__(cloud_pixels[i+j], whiteLED1[j])
            pixels.write()
            time.sleep(0.125)
    #shift its current color down an led every 3 leds like a wave
    x = True
    while x:
        for i in range(0, len(cloud_pixels), 3):
            for j in range(0,3):
                #print(whiteLED[j])
                pixels.__setitem__(cloud_pixels[i+j], whiteLED1[j])
                pixels.write()
            time.sleep(0.125)
        time.sleep(0.5)
        for i in range(0, len(cloud_pixels), 3):
            for j in range(0,3):
                #print(whiteLED[j])
                pixels.__setitem__(cloud_pixels[i+j], whiteLED2[j])
                pixels.write()
            time.sleep(0.125)
        time.sleep(0.5)
        for i in range(0, len(cloud_pixels), 3):
            for j in range(0,3):
                #print(whiteLED[j])
                pixels.__setitem__(cloud_pixels[i+j], whiteLED3[j])
                pixels.write()
            time.sleep(0.125)
        time.sleep(0.5)
        #x+=1

#nake a transition method between the weathers
#blink the current lights
#then show the new one, the specific one
# param: current, end
# type: string, string
# output: none
# type: none
# current is the type of lights currently on i.e. "sunny", "cloudy", "rainy"
# next has the same possible parameters
def transition(current, next):
    if(current == "sunny"):
        if(next == "cloudy"):
            for i in range(3):
                for i in sun_pixels:
                    pixels.__setitem__(i, ORANGE_RED)
                pixels.write()
                time.sleep(0.5)
                for i in sun_pixels:
                    pixels.__setitem__(i, NO_COLOR)
                pixels.write()
                time.sleep(0.5)
            time.sleep(0.25)
            cloudyDaySpecific()
        else:
            for i in range(3):
                for i in sun_pixels:
                    pixels.__setitem__(i, ORANGE_RED)
                pixels.write()
                time.sleep(0.5)
                for i in sun_pixels:
                    pixels.__setitem__(i, NO_COLOR)
                pixels.write()
                time.sleep(0.5)
            time.sleep(0.25)
            rainyDaySpecific()
    
    if(current == "cloudy"):
        if(next == "sunny"):
            for i in range(3):
                for i in cloud_pixels:
                    pixels.__setitem__(i, WHITE)
                pixels.write()
                time.sleep(0.5)
                for i in sun_pixels:
                    pixels.__setitem__(i, NO_COLOR)
                pixels.write()
                time.sleep(0.5)
            time.sleep(0.25)
            sunnyDaySpecific()
        else:
            for i in range(3):
                for i in cloud_pixels:
                    pixels.__setitem__(i, WHITE)
                pixels.write()
                time.sleep(0.5)
                for i in sun_pixels:
                    pixels.__setitem__(i, NO_COLOR)
                pixels.write()
                time.sleep(0.5)
            time.sleep(0.25)
            rainyDaySpecific()

    if(current == "rainy"):
        if(next == "cloudy"):
            for i in range(3):
                for i in rain_pixels:
                    pixels.__setitem__(i, BLUE)
                pixels.write()
                time.sleep(0.5)
                for i in sun_pixels:
                    pixels.__setitem__(i, NO_COLOR)
                pixels.write()
                time.sleep(0.5)
            time.sleep(0.25)
            cloudyDaySpecific()
        else:
            for i in range(3):
                for i in rain_pixels:
                    pixels.__setitem__(i, BLUE)
                pixels.write()
                time.sleep(0.5)
                for i in sun_pixels:
                    pixels.__setitem__(i, NO_COLOR)
                pixels.write()
                time.sleep(0.5)
            time.sleep(0.25)
            sunnyDaySpecific()


##method for turning on and off the lights not abrutly
# param: start, end, ONorOFF
# type: int, int
# output: none
# type: none
# start is the start number of the led
# end is the end number of the led
def onOrOff(start, end, ONorOFF):
    if(ONorOFF == "on" or ONorOFF == "oN" or ONorOFF == "On" or ONorOFF == "ON"):    
        for i in range(0,260,5):
            for j in range(start,end):
                pixels.__setitem__(j,(i,i,i))
            pixels.write()
    else:
        for i in range(255,-5,-5):
            for j in range(start,end):
                pixels.__setitem__(j,(i,i,i))
            pixels.write()

##main method
# param: none
# type: none
# output: none 
# type: none
def main():
    #clear()
    #showAllColors()
    #continuousStrip()    
    #rainHelper(LED_count)
    #rainyDay(0,100,"day","slow")
    sunnyDay(0,7)
    #cloudyDay(5,8)
    #onOrOff(3,20,"on")
    #onOrOff(3,20,"off")
    #clear()


##RUNTIME EXECUTIONS##
if __name__ == "__main__":
    main()
