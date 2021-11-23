# Establish Internet connection
from network import WLAN, STA_IF
import time

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

# @author Xavier Barneclo
# RPI to ESP32 communication, this is the ESP32 recieving

from mqttclient import MQTTClient
import time
import _thread
from LED_control import LED_control

def mqtt_thread():
    # helper function
    def thread_starter(theme):
        global thread
        thread = True

        _thread.start_new_thread(LED_thread, theme)

    # initalize session information
    session = "xbarneclo/moodlighting/comms"
    BROKER = "broker.mqttdashboard.com"
    qos = 2


    # connect to MQTT broker
    print("Connecting to MQTT broker", BROKER, "...", end="")
    mqtt = MQTTClient(BROKER, port=1883)
    mqtt.connect(BROKER, port=1883)
    print("Connected!")

    # lights turning on animation
    global thread
    thread = True

    thread_starter(4)

    # Define functions to execute when a message is recieved on a subscribed topic
    def theme_change(c, u, msg):
        theme = msg.decode('utf-8')

        # start by turning off thread
        global thread
        thread = False

        thread_starter(6)

        if theme == "Rainy":
            thread_starter(1)
        elif theme == "Sunny":
            thread_starter(2)
        else:
            thread_starter(3)
        
    def state_change(c, u, msg):
        input = msg.decode('utf-8')

        global thread
        thread = False

        if input == "on":
            # on transition here
            thread_starter(4)
        else:
            # off transition here
            thread_starter(5)


    # Topic subscriptions, if voice recognition isn't good enough implement adafruit IFTTT here
    state_topic = session + "/state"
    theme_topic = session + "/theme"
    mqtt.subscribe(state_topic)
    mqtt.subscribe(theme_topic)
    mqtt.message_callback_add(state_topic, state_change)
    mqtt.message_callback_add(theme_topic, theme_change)

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
