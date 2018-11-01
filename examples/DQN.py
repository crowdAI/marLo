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

import chainer

import gym

# gym.undo_logger_setup()  # NOQA
from gym import spaces
import gym.wrappers

import numpy as np
import marlo
from marlo import experiments
import time

parser = argparse.ArgumentParser(description='chainerrl dqn')

parser.add_argument('--n_hidden_channels', type=int, default=50, help='the number of hidden channels')
parser.add_argument('--n_hidden_layers', type=int, default=1, help='the number of hidden layers')
parser.add_argument('--results_dir', type=str, default="results", help='the results output dir')
parser.add_argument('--save_dir', type=str, default=None, help='the dir to save to or none')
parser.add_argument('--load_dir', type=str, default=None, help='the dir to save to or none.')
args = parser.parse_args()

# Tweakable parameters
n_hidden_channels = args.n_hidden_channels
n_hidden_layers = args.n_hidden_layers

print("n_hidden_channels " + str(n_hidden_channels) + " n_hidden_layers " + str(n_hidden_layers))
start_epsilon = 1.0
end_epsilon = 0.1
final_exploration_steps = 10 ** 5
out_dir = args.results_dir
gpu = 0
gamma = 0.99
replay_start_size = 1000
target_update_interval = 10 ** 2
update_interval = 1
target_update_method = 'hard'
soft_update_tau = 1e-2
rbuf_capacity = 5 * 10 ** 5
steps = 10 ** 6
eval_n_runs = 100
eval_interval = 10 ** 5

save_dir = args.save_dir


def phi(observation):
    return observation.astype(np.float32)


if not os.path.exists(out_dir):
    os.makedirs(out_dir)
out_dir_logs = out_dir + '/logging'
if not os.path.exists(out_dir_logs):
    os.makedirs(out_dir_logs)
if save_dir and not os.path.exists(save_dir):
    os.makedirs(save_dir)

experiments.set_log_base_dir(out_dir)

# Ensure that you have a minecraft-client running with : marlo-server --port 10000
# "MarLo-FindTheGoal-v0"
# 'MarLo-CatchTheMob-v0'
join_tokens = marlo.make("MarLo-FindTheGoal-v0",
                         params=dict(
                             allowContinuousMovement=["move", "turn"],
                             videoResolution=[84, 84],
                             kill_clients_after_num_rounds=500
                         ))
env = marlo.init(join_tokens[0])

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
    epsilon=0.001,
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

# Use GPU if any available
if gpu >= 0:
    chainer.cuda.get_device(gpu).use()
    q_func.to_gpu(gpu)

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

if args.load_dir:
    print("Loading model")
    agent.load(args.load_dir)

# Start training
experiments.train_agent_with_evaluation(
    agent=agent,
    env=env,
    eval_env=env,
    steps=steps,
    eval_n_runs=eval_n_runs,
    eval_interval=eval_interval,
    outdir=out_dir,
    max_episode_len=timestep_limit
)

if save_dir:
    print("Saving model")
    agent.save(save_dir)

# Draw the computational graph and save it in the output directory.
chainerrl.misc.draw_computational_graph(
    [q_func(np.zeros_like(obs_space.low, dtype=np.float32)[None])],
    os.path.join(out_dir, 'model')
)
