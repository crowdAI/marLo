#!/usr/bin/env python
import gym
from .main import MarloEnvBuilder


def _register():
    ##########################################
    # Version 0 of env 
    ##########################################
    gym.envs.registration.register(
        id='MarLo-DefaultWorld-v0',
        entry_point=MarloEnvBuilder,
        kwargs={
            "extra_params": {
                "reward_death": -10000,
                "reward_found_goal": 1000,
                "reward_out_of_time": -1000
            }
        },
    )
