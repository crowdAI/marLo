from chainerrl.agents.ddpg import DDPG
from chainerrl.agents.ddpg import DDPGModel
from chainerrl import experiments
from chainerrl import explorers
from chainerrl import misc
from chainerrl import policy
from chainerrl import q_functions
from chainerrl import replay_buffer

import chainer
from chainer import optimizers

import logging
import sys, os

import gym
gym.undo_logger_setup()  # NOQA
from gym import spaces
import gym.wrappers

import numpy as np
import marlo
import time

outdir = 'results'
gpu = None
final_exploration_steps = 10 ** 6
actor_lr = 1e-4
critic_lr = 1e-3
steps = 10 ** 7
n_hidden_channels = 300
n_hidden_layers = 3
replay_start_size = 5000
n_update_times = 1
target_update_interval = 1
target_update_method = 'soft' #can be 'hard' or 'soft'
soft_update_tau = 1e-2
update_interval = 4
eval_n_runs = 100
eval_interval = 10 ** 5
gamma = 0.995
minibatch_size = 200
reward_scale_factor = 1e-2

def phi(obs):
    return obs.astype(np.float32)

# Set filters
def clip_action_filter(a):
    return np.clip(a, action_space.low, action_space.high)

def reward_filter(r):
	return r * reward_scale_factor
	
# Ensure that you have a minecraft-client running with : marlo-server --port 10000
join_tokens = marlo.make('MinecraftCliffWalking1-v0', 
                params=dict(
                    allowContinuousMovement=["move", "turn"],
                    videoResolution=[800, 600]
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

timestep_limit = env.spec.tags.get(
        'wrapper_config.TimeLimit.max_episode_steps'
	)
obs_size = np.asarray(env.observation_space.shape).prod()
action_space = env.action_space
action_size = np.asarray(action_space.n).prod()

# Set the Q function up
q_func = q_functions.FCSAQFunction(
		obs_size, 
		action_size,
		n_hidden_channels=n_hidden_channels,
		n_hidden_layers=n_hidden_layers
	)
	
# Set the policy up
pi = policy.FCDeterministicPolicy(
		obs_size, 
		action_size=action_size,
		n_hidden_channels=n_hidden_channels,
		n_hidden_layers=n_hidden_layers,
		min_action=action_space.low, 
		max_action=action_space.high,
		bound_action=True
	)
	
# Set up the optimizers
opt_a = optimizers.Adam(alpha=actor_lr)
opt_c = optimizers.Adam(alpha=critic_lr)
opt_a.setup(model['policy'])
opt_c.setup(model['q_function'])
opt_a.add_hook(chainer.optimizer.GradientClipping(1.0), 'hook_a')
opt_c.add_hook(chainer.optimizer.GradientClipping(1.0), 'hook_c')

# Create the replay buffer
rbuf = replay_buffer.ReplayBuffer(5 * 10 ** 5)

# ------------ AGENT STARTUP -------------
def random_action():
	a = action_space.sample()
	if isinstance(a, np.ndarray):
		a = a.astype(np.float32)

	return a

# Instantiate the agent and explorer
ou_sigma = (action_space.high - action_space.low) * 0.2

explorer = explorers.AdditiveOU(sigma=ou_sigma)

agent = DDPG(
		model, 
		opt_a, 
		opt_c,
		rbuf, 
		gamma=gamma,
		explorer=explorer, 
		replay_start_size=replay_start_size,
		target_update_method=target_update_method,
		target_update_interval=target_update_interval,
		update_interval=update_interval,
		soft_update_tau=soft_update_tau,
		n_times_update=n_update_times,
		phi=phi, gpu=gpu, 
		minibatch_size=minibatch_size
	)

# Start evaluation
experiments.train_agent_with_evaluation(
		agent=agent, 
		env=env, 
		steps=steps,
		eval_env=env,
		eval_n_runs=eval_n_runs, 
		eval_interval=eval_interval,
		outdir=outdir,
		max_episode_len=timestep_limit
	)
