import time
from umqttsimple import MQTTClient
import ubinascii
import machine
from network import WLAN, STA_IF

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
topic_sub = "xbarneclo/testtopic/1"
topic_pub = "xbarneclo/testtopic/2"

last_message = 0
message_interval = 5
counter = 0

def sub_cb(topic, msg):
    print((topic, msg))


client = MQTTClient(client_id, mqtt_server)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic_sub)
print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))

while True:
    client.check_msg()
    client.publish(topic_pub, "aaaaaaa")
    time.sleep(1)