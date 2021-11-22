# @author Xavier Barneclo, Michael Jia
# LED control class

import machine
import neopixel
import math
import time

class LED_control:
    def __init__(self,c):
        self.LED_count = c

    def sunny_theme():
        a = 1

    def rainy_theme():
        a = 1

    def cloudy_theme():
        a = 1

    def on_transition():
        a = 1

    def off_transition():
        a = 1
    
    def theme_transition():
        a = 1

    def play_theme(self, theme):
        if theme == 1:
            self.sunny_theme()
        elif theme == 2:
            self.rainy_theme()
        elif theme == 3:
            self.cloudy_theme()
        elif 