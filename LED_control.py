# @author Xavier Barneclo, Michael Jia
# LED control class

import _thread
import math
import time

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
cloud_pixels = [8,9,10,11,12,13,14,15,16,19,24,31,34,41,46,55,58,63,70,73,74,75,76,77,78,79,80,81,82]
rain_pixels =[17,18,20,21,22,23,25,26,27,28,29,30,32,33,35,36,37,38,39,40,42,43,44,45,47,48,49,50,51,52,53,54,56,57,59,60,61,62,64,65,66,67,68,69,71,72] 

whiteLED1 = [DIMMER_WHITE4,DIMMER_WHITE2,WHITE]
whiteLED2 = [WHITE,DIMMER_WHITE4,DIMMER_WHITE2]
whiteLED3 = [DIMMER_WHITE2,DIMMER_WHITE4,WHITE]

class LED_control:
    def __init__(self,p):
        self.pixels = p
        self.lock = _thread.allocate_lock()
        self.state = None
        self.theme = None
       
    def sunny_theme(self):
        print("Playing sunny")
        pixels = self.pixels
        #turn on all the lights for the sun

        # for i in sun_pixels:
        #     #orange red light for the sun
        #     pixels.__setitem__(i, ORANGE_RED)
        # pixels.write()
        # time.sleep(0.25)
            
        #blink odd and evens on and off
        #alternating
        odds = []
        evens = []
        for i in sun_pixels:
            if(i%2 == 0):
                evens.append(i)
            else:
                odds.append(i)

        #turning light on and off alternating between odds and evens
        
        # turn odds on
        for i in odds:
            #orange red light for the sun
            pixels.__setitem__(i, ORANGE_RED)
        pixels.write()
        time.sleep(1)
        
        #turn odds off
        for i in odds:
            pixels.__setitem__(i, NO_COLOR)
        pixels.write()
        time.sleep(0.25)

        #turn evens on
        for i in evens:
            #orange red light for the sun
            pixels.__setitem__(i, ORANGE_RED)
        pixels.write()
        time.sleep(1)

        #turn evens off
        for i in evens:
            pixels.__setitem__(i, NO_COLOR)
        pixels.write()
        time.sleep(0.25)

        return False

    def rain_helper(self, length):
        #d = 0.5*g*t^2
        #generates the distances of the leds from the start (start is y = 0 meters)
        d = []
        for i in range(length+1):
            d.append(LED_distance*i)
        
        #generates the times for the particle to travel the distances
        t = []
        divisor = 0.5*gravity
        for i in [x/divisor for x in d]:
            t.append(math.sqrt(i))

        #generates the time intervals for the particle to travel in between the leds
        deltaT = []
        for i in range(len(t)-1):
            deltaT.append(t[i+1]-t[i])

        print(d)
        print(t)
        print(deltaT)

        return deltaT

    def rainy_theme(self, timeofday, speed):
        print("Playing rainy")
        pixels = self.pixels
        print(len(rain_pixels))
        time_interval = self.rain_helper(len(rain_pixels))
        if(speed == "slow" or speed == "Slow"):
            if(timeofday == "day" or timeofday == "Day"):
                for i in len(rain_pixels):
                    #blue light for the rain drop
                    pixels.__setitem__(rain_pixels[i], BLUE)
                    pixels.write()
                    time.sleep(time_interval[i]*20)
                    pixels.__setitem__(rain_pixels[i], NO_COLOR)
                    pixels.write()
            else:
                for i in len(rain_pixels):
                    #blue light for the rain drop
                    pixels.__setitem__(rain_pixels[i], DIMMER_BLUE)
                    pixels.write()
                    time.sleep(time_interval[i]*20)
                    pixels.__setitem__(rain_pixels[i], NO_COLOR)
                    pixels.write()
        else:
            if(timeofday == "day" or timeofday == "Day"):
                for i in len(rain_pixels):
                    #blue light for the rain drop
                    pixels.__setitem__(rain_pixels[i], BLUE)
                    pixels.write()
                    time.sleep(time_interval[i])
                    pixels.__setitem__(rain_pixels[i], NO_COLOR)
                    pixels.write()
            else:
                for i in len(rain_pixels):
                    #blue light for the rain drop
                    pixels.__setitem__(rain_pixels[i], DIMMER_BLUE)
                    pixels.write()
                    time.sleep(time_interval[i])
                    pixels.__setitem__(rain_pixels[i], NO_COLOR)
                    pixels.write()

        time.sleep(1)
        return False

    def cloudy_theme(self):
        print("Playing cloudy")
        pixels = self.pixels
        #shift its current color down an led every 3 leds like a wave
        for i in range(0, len(cloud_pixels), 3):
            for j in range(0,3):
                pixels.__setitem__(cloud_pixels[i+j], whiteLED1[j])
                pixels.write()
            time.sleep(0.125)
        time.sleep(0.5)
        for i in range(0, len(cloud_pixels), 3):
            for j in range(0,3):
                pixels.__setitem__(cloud_pixels[i+j], whiteLED2[j])
                pixels.write()
            time.sleep(0.125)
        time.sleep(0.5)
        for i in range(0, len(cloud_pixels), 3):
            for j in range(0,3):
                pixels.__setitem__(cloud_pixels[i+j], whiteLED3[j])
                pixels.write()
            time.sleep(0.125)
        time.sleep(0.5)
        return False

    def on_transition(self):
        print("Turning on")
        pixels = self.pixels
        for i in range(0,260,5):
            for j in range(len(pixels)):
                pixels.__setitem__(j,(i,i,i))
            pixels.write()
            
        for i in range(len(pixels)):
            pixels.__setitem__(i,(0,0,0))
        pixels.write()

    def off_transition(self):
        print("Turning off")
        pixels = self.pixels
        for i in range(255,-5,-5):
            for j in range(len(pixels)):
                pixels.__setitem__(j,(i,i,i))
            pixels.write()
        return True
    
    def theme_transition(self, curr_theme):
        print("Transitioning theme")
        pixels = self.pixels
        if(curr_theme == "Sunny"):
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
        elif(curr_theme == "Cloudy"):
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
        return True

    def play_theme(self):
        if self.state != None:
            if self.state_change:
                print("LED Thread: Changing state")
                if self.state == "on":
                    self.on_transition()
                else:
                    self.off_transition()
                self.state_change = False

        if self.theme != None and self.state != "off":
            print("LED Thread: Playing theme")
            if self.curr_theme != self.theme:
                self.theme_transition(self.curr_theme)

            if self.theme == "Sunny":
                return self.sunny_theme()
            elif self.theme == "Rainy":
                return self.rainy_theme("day","slow")
            elif self.theme == "Cloudy":
                return self.cloudy_theme()


    def update_theme(self, theme, curr_theme):
        self.theme = theme
        self.curr_theme = curr_theme

    def update_state(self, state):
        if state == "off" and self.state != "off":
            print("Internal state off")
            self.state = "off"
            self.state_change = True
        elif state == "on" and self.state != "on":
            print("Internal state on")
            self.state = "on"
            self.state_change = True

    def theme_control(self, theme, curr_theme, type):
        with self.lock:
            if type == 1:
                self.play_theme()
            elif type == 2:
                self.update_theme(theme, curr_theme)
            elif type == 3:
                self.update_state(theme)
