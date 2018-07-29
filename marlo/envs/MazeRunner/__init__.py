#!/usr/bin/env python
import gym
from .main import MarloEnvBuilder


def _register():
    ##########################################
    # Version 0 of env
    ##########################################
    gym.envs.registration.register(
        id='MazeRunner-v0',
        entry_point=MarloEnvBuilder,
        kwargs={
            "extra_params" : {
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
            "extra_params" : {
                "val1":"val1-alternate",
                "val2":"val2-alternate"
            }
        },
    )
