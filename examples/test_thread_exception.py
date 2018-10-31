
import marlo
import time


@marlo.threaded 
def run(i):
    time.sleep(3 + i)
    print("hick " + str(i))
    if i % 2 == 1:
        raise IOError("testing")


def check_for_exceptions(threads):
    for thread, queue in threads:
        if not thread.is_alive() and not queue.empty():
            result = queue.get()
            if isinstance(result, marlo.utils.ExceptionHolder):
                raise result.exception


thread_handlers = [run(i) for i in range(0, 2)]

for thread_handler in thread_handlers:
    t, q = thread_handler
    while t.is_alive():
        check_for_exceptions(thread_handlers)
        t.join(10)

check_for_exceptions(thread_handlers)

