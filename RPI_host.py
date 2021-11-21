# @author Xavier Barneclo
# RPI to ESP32 communication, this is the RPI sending

import paho.mqtt.client as paho
import time

# initalize session information
session = "xbarneclo/moodlighting/comms"
BROKER = "broker.mqttdashboard.com"
qos = 2

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, port=1883)
print("Connected!")

# initalize weather list
SUNNY_LIST = ["Sunny", "Fair", "Sun", "Clear"]
CLOUDY_LIST = ["Cloudy", "Overcast", "Clouds", "Mostly Cloudy", "Partly Cloudy", "Fog", "Haze", "Mist", "Smoke"]
RAINY_LIST = ["Rainy", "Rain", "Thunderstorm", "Lightning", "Snow", "Hail", "Sleet", "Sprinkling", "Drizzling", "Raining"]
THEME_LIST = [SUNNY_LIST,CLOUDY_LIST,RAINY_LIST]

# helper functions
def theme_select(msg):
    for i in THEME_LIST:
        for q in i:
            if msg == q:
                return i[0]

while True:
    # data collection: weather API
    mic_data = None


    # data collection: microphones
    weather_data = None
    theme = theme_select(weather_data)


    # publish if there is data
    mic_state = False
    weather_state = False

    if mic_state:
        mqtt.publish("{}/state".format(session), mic_data)

    if weather_state:
        mqtt.publish("{}/theme".format(session), weather_data)
