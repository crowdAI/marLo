#!/usr/bin/env python
import gym
from .main import MarloEnvBuilder


def _register():
    ##########################################
    # Version 0 of env 
    ##########################################
    gym.envs.registration.register(
        id='MarLo-Obstacles-v0',
        entry_point=MarloEnvBuilder,
        kwargs={
            "extra_params": {
            }
        },
    )
