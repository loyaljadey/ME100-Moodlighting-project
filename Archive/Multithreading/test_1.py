import _thread
from test_2 import data

d = data()

def iter():
    while True:
        print("Alt thread")
        d.iter(1)

def iter_1():
    while True:
        print("Main thread")
        d.iter(2)

_thread.start_new_thread(iter,())
iter_1()
