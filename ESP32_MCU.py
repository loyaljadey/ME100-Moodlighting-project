# @author Xavier Barneclo
# RPI to ESP32 communication, this is the ESP32 recieving

from mqttclient import MQTTClient
from machine import Pin
import time
import _thread
from LED_control import LED_control

def mqtt_thread():
    # initalize session information
    session = "xbarneclo/moodlighting/comms"
    BROKER = "broker.mqttdashboard.com"
    qos = 2

    global thread
    thread = True

    # connect to MQTT broker
    print("Connecting to MQTT broker", BROKER, "...", end="")
    mqtt = MQTTClient(BROKER, port=1883)
    mqtt.connect(BROKER, port=1883)
    print("Connected!")

    # Define function to execute when a message is recieved on a subscribed topic.
    def theme_change(c, u, msg):
        global thread
        thread = False

        theme = msg.decode('utf-8')

        _thread.start_new_thread(LED_thread, 6)

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
    global thread
    LED = LED_control()

    while thread:
        LED.play_theme(theme)
    _thread.exit()


_thread.start_new_thread(mqtt_thread,())
