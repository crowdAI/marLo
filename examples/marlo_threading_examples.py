#!/usr/bin/env python

import marlo
import time

@marlo.threaded
def example_function(agent_id):
    print("Agent-id : {}; sleeping for two seconds".format(agent_id))
    time.sleep(2)
    print("Exiting : {} ".format(agent_id))

thread_handler_1, _ = example_function(1)
thread_handler_2, _ = example_function(2)

thread_handler_1.join()
thread_handler_2.join()

print("Code Exit")
