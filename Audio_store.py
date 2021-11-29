import threading

class storage():
    def __init__(self):
        self.audio = None
        self.mic_lock = threading.Lock()
        self.MQTT_lock = threading.Lock()
        self.MQTT_lock.acquire()

    def get_audio(self):
        self.MQTT_lock.acquire()
        ret_audio = self.audio
        self.mic_lock.release()
        return ret_audio

    def set_audio(self, audio):
        self.mic_lock.acquire()
        self.audio = audio
        self.MQTT_lock.release()
