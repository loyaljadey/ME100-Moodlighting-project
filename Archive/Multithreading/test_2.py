import _thread
import time

class data:
    def __init__(self):
        self.a = 1
        self.lock = _thread.allocate_lock()

    def iter(self, item):
        with self.lock:
            self.a += 1
            time.sleep(5)
        print(self.a)

    def thread_one(self):
        time.sleep(5)

    def thread_two(self):
        time.sleep(5)

