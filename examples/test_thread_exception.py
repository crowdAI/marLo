
import marlo
import time


@marlo.threaded 
def run(i):
    time.sleep(3 + i)
    print("hick " + str(i))
    if i % 2 == 1:
        raise IOError("testing")


thread_handlers = [run(i) for i in range(0, 2)]

marlo.utils.join_all(thread_handlers)
