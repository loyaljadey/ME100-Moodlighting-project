# @author Xavier Barneclo
# RPI to ESP32 communication, this is the ESP32 recieving

from mqttclient import MQTTClient
from machine import Pin
import time
import _thread

def mqtt_thread():
    # initalize session information
    session = "xbarneclo/moodlighting/comms"
    BROKER = "broker.mqttdashboard.com"
    qos = 2

    global thread
    thread = None

    # connect to MQTT broker
    print("Connecting to MQTT broker", BROKER, "...", end="")
    mqtt = MQTTClient(BROKER, port=1883)
    mqtt.connect(BROKER, port=1883)
    print("Connected!")

    # Define function to execute when a message is recieved on a subscribed topic.
    def theme_change(c, u, msg):
        theme = msg.decode('utf-8')
        # TO-DO: transition code here

        global thread
        if thread:
            thread.exit()

        if theme == "Rainy":
            thread = _thread.start_new_thread(LED_thread, 1)
        elif theme == "Sunny":
            thread = _thread.start_new_thread(LED_thread, 2)
        else:
            thread = _thread.start_new_thread(LED_thread, 3)
        
    def state_change(c, u, msg):
        input = msg.decode('utf-8')
        if input == "on":
            return None
            # on transition here
        else:
            return None
            # off transition here

    # Topic subscriptions, if voice recognition isn't good enough implement adafruit IFTTT here
    state_topic = session + "/state"
    theme_topic = session + "/theme"
    mqtt.subscribe(state_topic)
    mqtt.subscribe(theme_topic)
    mqtt.message_callback_add(state_topic, state_change)
    mqtt.message_callback_add(theme_topic, theme_change)

    mqtt.loop_forever()

def LED_thread(theme):
    if theme == 1:
        while True:
            # Rainy LED code
            a = 1;
    elif theme == 2:
        while True:
            # Sunny LED code
            a = 1
    else:
        while True:
            # Cloudy LED code
            a = 1

_thread.start_new_thread(mqtt_thread,())
