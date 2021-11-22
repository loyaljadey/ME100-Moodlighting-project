import _thread
import time

class thread_test:
    def __init__(self,a):
        self.a = a

    def print(self):
        print("yay")
        time.sleep(.5)