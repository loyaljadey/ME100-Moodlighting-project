# @author Xavier Barneclo
# RPI to ESP32 communication, this is the ESP32 recieving

from mqttclient import MQTTClient
import _thread
from LED_control import LED_control
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
from network import WLAN, STA_IF

RAINY = 1
SUNNY = 2
CLOUDY = 3
ON = 4
OFF = 5
TRANS = 6



def mqtt_thread():
    # helper function
    def thread_starter(theme):
        global thread
        thread = True

        _thread.start_new_thread(LED_thread, theme)

    wlan = WLAN(STA_IF)
    wlan.active(True)

    wlan.connect('Weefee', 'barnacles')

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
        state = msg
        theme = msg

        # start by turning off thread
        global thread
        thread = False

        # transition theme anmiation
        thread_starter(TRANS)

        # change state
        if input == "on":
            # on transition here
            thread_starter(ON)
        else:
            # off transition here
            thread_starter(OFF)
        
        # change theme
        if theme == "Rainy":
            thread_starter(RAINY)
        elif theme == "Sunny":
            thread_starter(SUNNY)
        else:
            thread_starter(CLOUDY)


    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))


    # lights turning on animation
    thread_starter(ON)

    while True:
        client.check_msg()
        time.sleep(5)


def LED_thread(theme):
    global thread
    LED = LED_control()

    out = None
    while thread and not out:
        out = LED.play_theme(theme)
    _thread.exit()


_thread.start_new_thread(mqtt_thread,())

while True:
    pass