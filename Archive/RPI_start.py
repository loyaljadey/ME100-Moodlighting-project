import subprocess
import time

subprocess.call('sudo cp /home/pi/archive.txt /home/pi/.asoundrc', shell=True)
time.sleep(1)
subprocess.call('python /home/pi/ME100-Moodlighting-project/RPI_host.py',)