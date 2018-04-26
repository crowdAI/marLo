#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
import os
import numpy as np

import logger
logger = logging.getLogger(__name__)

import gym
from gym import spaces, error

try:
    import MalmoPython as MP
except ImportError as e:
    raise error.DependencyNotInstalled(
        "MalmoPython doesnt seem to be installed. Please follow the \
        instructions at https://github.com/spMohanty/marLo#env-setup.")

TOTAL_TIME_STEPS = 1000


class MarloBaseEnv(gym.Env):
    """
    Define a base environment class for Marlo Envs
    """
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, marlo_env_spec):
        super(MarloBaseEnv, self).__init__()

        self.__version__ = "0.1.0"
        print("MarloBaseEnv - Version {}".format(self.__version__))

        # Initialize Marlo Mission
        self.load_mission_spec(marlo_env_spec)

        # General variables defining the environment
        self.action_space = spaces.Discrete(10)

        # Observation is the remaining time
        low = np.array([0.0,  # remaining_tries
                        ])
        high = np.array([self.TOTAL_TIME_STEPS,  # remaining_tries
                         ])
        self.observation_space = spaces.Box(low, high)

        # Store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory = []
        self.is_done = False

    def load_mission_spec(self, marlo_env_spec):
        path_to_env_spec = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "marlo_env_specs",
            marlo_env_spec
        )
        marlo_env_spec = open(path_to_env_spec, "r").read()
        self.mission_spec = MP.MissionSpec(marlo_env_spec, True)

    def _step(self, action):
        """
        The agent takes a step in the environment.
        Parameters
        ----------
        action : int
        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        self.curr_step += 1
        self._take_action(action)
        reward = self._get_reward()
        ob = self._get_state()
        return ob, reward, self.is_done, {}

    def _take_action(self, action):
        """Take Action"""
        pass

    def _get_reward(self):
        """Reward is given for a sold banana."""
        return np.random.rand()

    def _reset(self):
        """
        Reset the state of the environment and returns an initial observation.
        Returns
        -------
        observation (object): the initial observation of the space.
        """
        self.curr_episode += 1
        self.action_episode_memory.append([])
        self.is_done = False
        return self._get_state()

    def _render(self, mode='human', close=False):
        return

    def _get_state(self):
        """Get the observation."""
        ob = [self.TOTAL_TIME_STEPS - self.curr_step]
        return ob

    def _seed(self, seed):
        random.seed(seed)
        np.random.seed(seed)
