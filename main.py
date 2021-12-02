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

pin = 27
LED_count = 83


term = True
pixels = neopixel.NeoPixel(machine.Pin(pin), LED_count)

LED = LED_control(pixels)

def mqtt_thread():
    # helper function
    wlan = WLAN(STA_IF)
    wlan.active(True)

    a = wlan.scan()

    wifi_store = [['ME100-2.4G', '122Hesse'],['NETGEAR78X','jmacxb301324'],['room4s', 'SphstakesonBerk1']]

    for i in a:
        for q in wifi_store:
            if i[0].decode('UTF-8') == q[0]:
                wlan.connect(q[0], q[1])

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
        if state == "on" or state == "off":
            # on/off transition here
            LED.theme_control(state, theme, 3)
        elif theme != curr_theme:
            LED.theme_control(theme, curr_theme, 2)


    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))

    try:
        while True:
            print("waiting for command")
            client.check_msg()
            time.sleep(.25)
    except:
        machine.reset()


def LED_thread():
    while True:
        LED.theme_control(None, None, 1)

print("Starting MQTT Thread")
_thread.start_new_thread(mqtt_thread, ())
print("Starting LED control")
LED_thread()