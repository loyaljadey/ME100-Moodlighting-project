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