from marlo import experiments

from chainerrl.agents.dqn import DQN
from chainerrl import explorers
from chainerrl import links
from chainerrl import misc
from chainerrl import q_functions
from chainerrl import replay_buffer
from chainer import optimizers
import chainerrl
import logging
import sys
import os
import argparse

import gym

gym.undo_logger_setup()  # NOQA
from gym import spaces
import gym.wrappers

import numpy as np
import marlo
import time
from marlo.multiagent import start_agents
from gym.envs.registration import register

# Tweakable parameters
n_hidden_channels = 100
n_hidden_layers = 2
start_epsilon = 1.0
end_epsilon = 0.1
final_exploration_steps = 10 ** 2
outdir = 'results'
gpu = None
gamma = 0.99
replay_start_size = 1000
target_update_interval = 10 ** 2
update_interval = 1
target_update_method = 'hard'
soft_update_tau = 1e-2
rbuf_capacity = 5 * 10 ** 5
max_steps = 10 ** 8  # set really high so that we do the specified number of rollouts
eval_n_runs = 10
eval_interval = 10 ** 4


def phi(obs):
    return obs.astype(np.float32)


parser = argparse.ArgumentParser(description='Multi-agent chainerrl DQN example')
# Example missions: 'pig_chase.xml' or 'bb_mission_1.xml' or 'th_mission_1.xml'
parser.add_argument('--rollouts', type=int, default=1, help='number of rollouts')
parser.add_argument('--mission_file', type=str, default="basic.xml", help='the mission xml')
parser.add_argument('--turn_based', action='store_true')
args = parser.parse_args()


turn_based = args.turn_based
number_of_rollouts = args.rollouts

# Register the multi-agent environment.
env_name = 'malmo-multi-agent-v0'

register(
    id=env_name,
    entry_point='marlo.envs:MinecraftEnv',
    # Make sure mission xml is in the marlo/assets directory.
    kwargs={'mission_file': args.mission_file}
)

env = marlo.make(env_name)

resolution = [84, 84]  # [800, 600]
config = {'allowDiscreteMovement': ["move", "turn"], 'videoResolution': resolution, "turn_based": turn_based}

join_agents = start_agents(env, env_name, None, config, number_of_rollouts + 1, daemon=True)

env.init(**config)

obs = env.reset()
env.render(mode="rgb_array")
print('initial observation:', obs)

action = env.action_space.sample()
obs, r, done, info = env.step(action)
print('next observation:', obs)
print('reward:', r)
print('done:', done)
print('info:', info)

print('actions:', str(env.action_space))
print('sample action:', str(env.action_space.sample))

# run first episode to reset
while not done:
    action = env.action_space.sample()
    obs, r, done, info = env.step(action)

print("Setup for training")

timestep_limit = env.spec.tags.get('wrapper_config.TimeLimit.max_episode_steps')
obs_space = env.observation_space
obs_size = obs_space.low.size
action_space = env.action_space

n_actions = action_space.n
q_func = q_functions.FCStateQFunctionWithDiscreteAction(
    obs_size, n_actions,
    n_hidden_channels=n_hidden_channels,
    n_hidden_layers=n_hidden_layers
)

# Use epsilon-greedy for exploration
# Constant
explorer = explorers.ConstantEpsilonGreedy(
    epsilon=0.3,
    random_action_func=env.action_space.sample
)

# Linear decay
# explorer = explorers.LinearDecayEpsilonGreedy(
# start_epsilon,
# end_epsilon,
# final_exploration_steps,
# random_action_func=str(env.action_space.sample)
# )

# Set up Adam optimizer
opt = optimizers.Adam()
opt.setup(q_func)

# DQN uses Experience Replay.
# Specify a replay buffer and its capacity.
rbuf = chainerrl.replay_buffer.ReplayBuffer(capacity=rbuf_capacity)

# Initialize the agent
agent = DQN(
    q_func, opt, rbuf,
    gpu=gpu,
    gamma=gamma,
    explorer=explorer,
    replay_start_size=replay_start_size,
    target_update_interval=target_update_interval,
    update_interval=update_interval,
    phi=phi,
    target_update_method=target_update_method,
    soft_update_tau=soft_update_tau,
    episodic_update_len=16
)

print("train...")

# Start training
experiments.train_agent_with_evaluation(
    agent=agent,
    env=env,
    eval_env=env,
    steps=max_steps,
    eval_n_runs=eval_n_runs,
    eval_interval=eval_interval,
    outdir=outdir,
    max_episode_len=timestep_limit,
    num_resets=number_of_rollouts
)

print("training done")

join_agents()

# Draw the computational graph and save it in the output directory.
chainerrl.misc.draw_computational_graph(
    [q_func(np.zeros_like(obs_space.low, dtype=np.float32)[None])],
    os.path.join(outdir, 'model')
)
