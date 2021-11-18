import machine, neopixel
import time

LED_count = 300
pin = 18

pixels = neopixel.NeoPixel(machine.Pin(pin), LED_count)


def continuousStrip():
    for i in range(LED_count):
        pixels[i] = (255,0,0)
        pixels.write()
        time.sleep(0.5)


def rainyDay():
    for i in range(LED_count):
        pixels[i] = (255,0,0)
        pixels.write()
        time.sleep(0.25)