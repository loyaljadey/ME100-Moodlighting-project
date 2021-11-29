# @author Xavier Barneclo
# RPI to ESP32 communication, this is the ESP32 recieving

import _thread
from LED_control import LED_control
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
from network import WLAN, STA_IF
import neopixel

RAINY = 2
SUNNY = 1
CLOUDY = 3
ON = 4
OFF = 5
TRANS = 6

pin = 27
LED_count = 83



def mqtt_thread():
    # create pixels object for continuous use between threads
    pixels = neopixel.NeoPixel(machine.Pin(pin), LED_count)

    # helper function
    def thread_starter(theme, curr_theme):
        global thread
        thread = True

        _thread.start_new_thread(LED_thread, (theme, pixels, curr_theme))

    def thread_off():
        global thread
        thread = False

    wlan = WLAN(STA_IF)
    wlan.active(True)

    wlan.connect('NETGEAR78X', 'jmacxb301324')

    tries = 0
    while not wlan.isconnected() and tries < 10:
        print("Waiting for wlan connection")
        time.sleep(1)
        tries = tries + 1

    if wlan.isconnected():
        print("WiFi connected at", wlan.ifconfig()[0])
    else:
        print("Unable to connect to WiFi")

    client_id = ubinascii.hexlify(machine.unique_id())
    mqtt_server = "broker.mqttdashboard.com"
    topic_sub = "xbarneclo/RPI2ESP/state"


    def sub_cb(topic, msg):
        # extract relevant information from MQTT message
        message = msg.decode('UTF-8')
        message = message.split(',')
        state = message[0]
        curr_theme = message[2]
        theme = message[1]

        print(message)
        print(state)
        print(theme)
        print(curr_theme)


        # change state
        if state == "on":
            # on transition here
            thread_off()
            thread_starter(ON, None)
        elif state == "off":
            # off transition here
            thread_off()
            thread_starter(OFF, None)
        
        # change theme
        if theme == "Rainy":
            thread_off()
            thread_starter(TRANS, curr_theme)
            thread_starter(RAINY, None)
        elif theme == "Sunny":
            thread_off()
            thread_starter(TRANS, curr_theme)
            thread_starter(SUNNY, None)
        elif theme == "Cloudy":
            thread_off()
            thread_starter(TRANS, curr_theme)
            thread_starter(CLOUDY, None)


    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))


    # lights turning on animation
    thread_starter(ON, None)

    try:
        while True:
            print("waiting for command")
            client.wait_msg()
            time.sleep(1)
    except:
        machine.reset()


def LED_thread(theme, pixels, curr_theme):
    global thread
    LED = LED_control(pixels)

    out = None
    while thread and not out:
        out = LED.play_theme(theme, curr_theme)
    print("thread killed")
    _thread.exit()


_thread.start_new_thread(mqtt_thread,())

while True:
    pass