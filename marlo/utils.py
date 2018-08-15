#!/usr/bin/env python
import gym
import marlo
import sys
import os
import importlib
import logging
logger = logging.getLogger(__name__)

from threading import Thread
from queue import Queue

import socket
from contextlib import closing

from marlo.launch_minecraft_in_background import launch_minecraft_in_background

def register_environments(MARLO_ENV_PATHS):
    """Searches for Marlo Environments in the provided paths, and registers
    them as valid MarLo environments to be used by `marlo.make`.

    Expect that each env directory will have the relevant 
    gym registrations implemented in ``__init__.py`` 
    and a ``main.py`` will implement a derived class of 
    :class:`marlo.base_env_builder.MarloEnvBuilderBase` with the necessary 
    functions overriden.


    :param MARLO_ENV_PATHS: Path to directory containing multiple MarLo envs
    :type number_of_clients: str
    
    :rtype:  None
    """        
    for env_path in MARLO_ENV_PATHS:
        sys.path.append(env_path)
        for _marlo_env_dir in os.listdir(env_path):
            """
            Expect that each env directory will have the relevant 
            gym registrations implemented in __init__.py 
            and a `main.py` will implement a derived class of 
            :class:`marlo.base_env_builder.MarloEnvBuilderBase`.
            """
            if os.path.isdir(os.path.join(env_path, _marlo_env_dir)) and \
                    not str(_marlo_env_dir).startswith("__"):
                module = importlib.import_module(_marlo_env_dir)
                module._register()
                logger.debug("Creating envs from : {}".format(_marlo_env_dir))

def threaded(fn):
    """Implements the ``@marlo.threaded`` decorator to help easily run functions in a 
    separate thread. Useful in multiagent scenarios when we want to run 
    multiple blocking agents across different threads.

    .. code-block:: python

        import marlo

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

    :param fn: Function defitnion 
    :type fn: func
    
    :returns thread_handler to join the threads if required
    """
    def wrap(queue, *args, **kwargs):
        queue.put(fn(*args, **kwargs))

    def call(*args, **kwargs):
        queue = Queue()
        job = Thread(target=wrap, args=(queue,) + args, kwargs=kwargs)
        job.start()
        return job, queue

    return call

def find_free_port():
    """Find a random free port where a Minecraft Client can possibly be launched.
    
    :rtype:  `int`
    """    
    
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def launch_clients(number_of_clients, replaceable=False):
    """Launches a series of Minecraft Client which can be used by 
    MarLo environments.

    :param number_of_clients: Number of Minecraft Clients to launch
    :type number_of_clients: int
    :param replaceable: `replaceable` argument from `launchClient.sh` (TODO: Check with @Andre)
    :type replaceable: bool

    **Note** This is still in experimental phase, as this does not yet clean up 
    the processes after the code exits.
    
    :returns:  A valid `client_pool` object ( a `list` of `tuples`)

    >>> import marlo
    >>> client_pool = marlo.launch_clients(number_of_client=2)
    >>> print(client_pool)
    >>> [('127.0.0.1', 27655), ('127.0.0.1', 15438)]
    """    
    ports = [find_free_port() for _ in range(number_of_clients)]
    MINECRAFT_ROOT = os.getenv("MALMO_MINECRAFT_ROOT")
    if not MINECRAFT_ROOT:
        raise Exception("Please set the environment variable"
                        "`MALMO_MINECRAFT_ROOT` as the root of your "
                        "Minecraft Directory")

    launch_processes = launch_minecraft_in_background(
                            MINECRAFT_ROOT,
                            ports,
                            replaceable=False
                            )

    client_pool = [('127.0.0.1', port) for port in ports]
    return client_pool
