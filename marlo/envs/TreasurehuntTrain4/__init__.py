
import gym
from .main import MarloEnvBuilder


def _register():
    ##########################################
    # Version 0 of env
    ##########################################
    gym.envs.registration.register(
        id='MarLo-TreasurehuntTrain4-v0',
        entry_point=MarloEnvBuilder
    )
