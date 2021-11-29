# @author Xavier Barneclo
# RPI to ESP32 communication, this is the RPI sending

import paho.mqtt.client as paho
from Weather_API import Weather_API
import speech_recognition as sr
import time


# initalize session information
session = "xbarneclo/RPI2ESP/state"
BROKER = "broker.mqttdashboard.com"
qos = 0

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, port=1883)
print("Connected!")

r = sr.Recognizer()
mic = sr.Microphone(device_index=11)

prev_weather = None
prev_mic = None

bing_key = '6267bba0804e4750a10c71224de92fad'

while True:
    # data collection: microphones
    # should be on, off, or None output
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("recording")
        audio = r.record(source, offset =.5, duration = 3)

    print("analyzing")
    try:
        text = r.recognize_bing(audio, key=bing_key)
        text = text.replace('.','')
        text = text.lower()
        if text == "on" or text == "off" or text == "turn on" or text == "turn off":
            mic_data = text
        else:
            mic_data = None
    except:
        mic_data = None

    if (mic_data == None or mic_data == "off") and (prev_mic == "off" or prev_mic == "stay off"):
        mic_data = "stay off"

    if (mic_data == None or mic_data == "on") and (prev_mic == "on" or prev_mic == "stay on"):
        mic_data = "stay on"


    # data collection: weather API
    weather = Weather_API()
    weather_data = weather.get_theme()


    # publish if there is changed data
    if prev_mic != mic_data or prev_weather != weather_data:
        if mic_data == "off" or mic_data == "stay off":
            mqtt.publish(session, "{},{},{}".format(mic_data, None, prev_weather))
        else:
            mqtt.publish(session, "{},{},{}".format(mic_data, weather_data, prev_weather))
        prev_mic = mic_data
        prev_weather = weather_data
