import _thread
import time
from thread_testing_two import thread_test


def thread_one():
    print("Opening thread two")

    global a
    a = True

    _thread.start_new_thread(thread_two,())
    time.sleep(2)

    
    a = False

    _thread.exit()

def thread_two():
    global a

    test = thread_test(a)
    while a:
        test.print()

    print("Successfully modified sub thread and method from main thread")
    _thread.interrupt_main()
    

print("Opening thread one")
_thread.start_new_thread(thread_one,())

while True:
    pass
