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
        print("sunny theme")
        return False

    def rainy_theme():
        print("rainy theme")
        return False

    def cloudy_theme():
        print("sunny theme")
        return False

    def on_transition():
        print("on transition")
        return True

    def off_transition():
        print("off transition")
        return True
    
    def theme_transition():
        print("theme transition")
        return True

    def play_theme(self, theme):
        if theme == 1:
            self.sunny_theme()
        elif theme == 2:
            self.rainy_theme()
        elif theme == 3:
            self.cloudy_theme()
        elif theme == 4:
            self.on_transition()
        elif theme == 5:
            self.off_transition()
        else:
            self.theme_transition()