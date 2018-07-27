#!/usr/bin/env python
import gym
from .main import MarloEnvBuilder

MOHANTY="something"

def _register():
    ##########################################
    # Version 0 of env
    ##########################################
    gym.envs.registration.register(
        id='MazeRunner-v0',
        entry_point=MarloEnvBuilder,
        max_episode_steps=1000,
        reward_threshold=1000,
        kwargs={
            "extra_param" : {
                "val1":"val1",
                "val2":"val2"
            }
        },
    )

    ##########################################
    # Version 1 of env
    ##########################################
    gym.envs.registration.register(
        id='MazeRunner-v1',
        entry_point=MarloEnvBuilder,
        kwargs={
            "extra_param" : {
                "val1":"val1-alternate",
                "val2":"val2-alternate"
            }
        },
    )
