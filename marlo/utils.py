#!/usr/bin/env python
import gym
import sys
import os
import importlib
import logging
logger = logging.getLogger(__name__)

def register_environments(MARLO_ENV_PATHS):
    for env_path in MARLO_ENV_PATHS:
        sys.path.append(env_path)
        for _marlo_env_dir in os.listdir(env_path):
            """
            Expect that each env directory will have the relevant 
            gym registrations in a "register_environments" functions 
            implemented in __init__.py
            """
            if os.path.isdir(os.path.join(env_path, _marlo_env_dir)) and \
                    not _marlo_env_dir.startswith("__"):
                module = importlib.import_module(_marlo_env_dir)
                module._register()
                logger.debug("Creating envs from : {}".format(_marlo_env_dir))
