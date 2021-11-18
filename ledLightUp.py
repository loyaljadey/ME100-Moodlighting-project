import machine
import neopixel
import time

LED_count = 10
pin = 27

pixels = neopixel.NeoPixel(machine.Pin(pin), LED_count)

def clear():
    for i in range(LED_count):
        print("clearing")
        pixels[i] = (0,0,0)
        pixels.write()
        #time.sleep(0.5)
    print("cleared")

def continuousStrip():
    for i in range(LED_count):
        print("strip")
        pixels[i] = (255,0,0)
        pixels.write()
        time.sleep(0.5)

def rainyDay():
    for i in range(LED_count):
        pixels[i] = (255,0,0)
        pixels.write()
        time.sleep(0.25)

def showAllColors():
    for i in range(LED_count):
        print("showing")
        pixels[i] = (0, 0, 255)
        pixels.write()
        time.sleep(0.5)


def main():
    # clear()
    # continuousStrip()
    # clear()
    showAllColors()

if __name__ == "__main__":
    main()
