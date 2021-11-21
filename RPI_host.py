# @author Xavier Barneclo
# RPI to ESP32 communication, this is the RPI sending

import paho.mqtt.client as paho
from Weather_API import Weather_API


# initalize session information
session = "xbarneclo/moodlighting/comms"
BROKER = "broker.mqttdashboard.com"
qos = 2

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, port=1883)
print("Connected!")

prev_mic = None
prev_state = None

while True:
    # data collection: microphones
    mic_data = None


    # data collection: weather API
    weather = Weather_API()
    weather_data = weather.get_theme()


    # publish if there is data
    mic_state = False
    weather_state = False

    if mic_state:
        mqtt.publish("{}/state".format(session), mic_data)

    if weather_state:
        mqtt.publish("{}/theme".format(session), weather_data)
