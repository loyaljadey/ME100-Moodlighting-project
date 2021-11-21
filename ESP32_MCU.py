# @author Xavier Barneclo
# RPI to ESP32 communication, this is the ESP32 recieving

from mqttclient import MQTTClient
import sys
from machine import Pin
import time

# initalize session information
session = "xbarneclo/moodlighting/comms"
BROKER = "broker.mqttdashboard.com"
qos = 2

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(BROKER, port=1883)
mqtt.connect(BROKER, port=1883)
print("Connected!")

# Define function to execute when a message is recieved on a subscribed topic.
def theme_change(c, u, msg):
    msg.decode('utf-8')
    # TO-DO: transition code here

    #TO-DO: theme code here
    

def state_change(c, u, msg):
    msg.decode('utf-8')
    # TO-DO: transition code here



# Topic subscriptions, if voice recognition isn't good enough implement adafruit IFTTT here
state_topic = session + "/state"
theme_topic = session + "/theme"
mqtt.subscribe(state_topic)
mqtt.subscribe(theme_topic)
mqtt.message_callback_add(state_topic, state_change)
mqtt.message_callback_add(theme_topic, theme_change)

mqtt.loop_forever()