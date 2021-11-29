# @author Xavier Barneclo
# RPI to ESP32 communication, this is the RPI sending

import paho.mqtt.client as paho
from Weather_API import Weather_API
import speech_recognition as sr
import time
import threading
from Audio_store import storage


# initalize session information
session = "xbarneclo/RPI2ESP/state"
BROKER = "broker.mqttdashboard.com"
qos = 0

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, port=1883)
print("Connected!")


prev_weather = None
prev_mic = None

bing_key = '6267bba0804e4750a10c71224de92fad'

store = storage()

def mic_thread(name):
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=11)
    while True:
        # data collection: microphones
        # should be on, off, or None output
        with mic as source:
            print("Recording")
            r.adjust_for_ambient_noise(source)
            audio = r.record(source, offset =.5, duration = 3)
            print("Waiting to send audio")
            store.set_audio(audio)
            
            

def MQTT_thread():
    weather_cycle = 0
    while True:
        print("Waiting to receive audio")
        audio = store.get_audio()
        print("Analyzing audio")
        try:
            text = r.recognize_bing(audio, key=bing_key)
            text = text.replace('.','')
            text = text.lower()
            if text == "on" or text == "turn on":
                mic_data = "on"
            elif text == "off" or text == "turn off":
                mic_data = "off"
            else:
                mic_data = None
        except:
            mic_data = None


        # data collection: weather API
        if weather_cycle == 0:
            weather = Weather_API()
            weather_data = weather.get_theme()
            weather_cycle = 10
        weather_cycle -= 1

        # publish if there is changed data
        print("Publishing to MQTT")
        if prev_mic != mic_data or prev_weather != weather_data:
            mqtt.publish(session, "{},{},{}".format(mic_data, weather_data, prev_weather))
        else:
            mqtt.publish(session, "{},{},{}".format(None, None, None))

        prev_mic = mic_data
        prev_weather = weather_data

mic = threading.Thread(target=mic_thread, args=(1,))
mic.start()

MQTT_thread()