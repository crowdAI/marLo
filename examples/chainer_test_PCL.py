import chainerrl
from chainerrl import experiments
from chainerrl import misc
from chainerrl.optimizers import rmsprop_async

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
gpu = 0
batchsize = 10
rollout_len = 10
n_hidden_channels = 100
n_hidden_layers = 2
n_times_replay = 1
replay_start_size = 10000
t_max = None
tau = 1e-2
steps = 8 * 10 ** 7
eval_interval = 10 ** 5
eval_n_runs = 10
reward_scale_factor = 1e-2
render = False
lr = 7e-4
prioritized_replay = False
disable_online_update = False
backprop_future_values = True

def phi(obs):
    return obs.astype(np.float32)
	
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

# Set environment related spaces
timestep_limit = env.spec.tags.get(
		'wrapper_config.TimeLimit.max_episode_steps'
	)
obs_space = env.observation_space
action_space = env.action_space

# Switch policy types accordingly to action space types
if isinstance(action_space, gym.spaces.Box):
	model = chainerrl.agents.pcl.PCLSeparateModel(
		pi=chainerrl.policies.FCGaussianPolicy(
			obs_space.low.size, action_space.low.size,
			n_hidden_channels=n_hidden_channels,
			n_hidden_layers=n_hidden_layers,
			bound_mean=True,
			min_action=action_space.low,
			max_action=action_space.high,
			var_wscale=1e-3,
			var_bias=1,
			var_type='diagonal',
		),
		v=chainerrl.v_functions.FCVFunction(
			obs_space.low.size,
			n_hidden_channels=n_hidden_channels,
			n_hidden_layers=n_hidden_layers,
		)
	)
else:
	model = chainerrl.agents.pcl.PCLSeparateModel(
		pi=chainerrl.policies.FCSoftmaxPolicy(
			obs_space.low.size, action_space.n,
			n_hidden_channels=n_hidden_channels,
			n_hidden_layers=n_hidden_layers
		),
		v=chainerrl.v_functions.FCVFunction(
			obs_space.low.size,
			n_hidden_channels=n_hidden_channels,
			n_hidden_layers=n_hidden_layers,
		),
	)

# Setup the optimizer
opt = chainer.optimizers.Adam(alpha=lr)
opt.setup(model)
	
# Use GPU if any available
if gpu >= 0:
	chainer.cuda.get_device(gpu).use()
	model.to_gpu(gpu)

# Initialize the buffer
if prioritized_replay:
	replay_buffer = \
		chainerrl.replay_buffer.PrioritizedEpisodicReplayBuffer(
			capacity=5 * 10 ** 3,
			uniform_ratio=0.1,
			default_priority_func=exp_return_of_episode,
			wait_priority_after_sampling=False,
			return_sample_weights=False)
else:
	replay_buffer = chainerrl.replay_buffer.EpisodicReplayBuffer(
			capacity=5 * 10 ** 3
		)
		
# Initialize the agent
agent = chainerrl.agents.PCL(
        model, opt, replay_buffer=replay_buffer,
        t_max=t_max, 
		gamma=0.99,
        tau=tau,
        phi=phi,
        rollout_len=rollout_len,
        n_times_replay=n_times_replay,
        replay_start_size=replay_start_size,
        batchsize=batchsize,
        disable_online_update=disable_online_update,
        backprop_future_values=backprop_future_values,
    )
	
# Start training
experiments.train_agent_with_evaluation(
		agent=agent,
		env=env,
		eval_env=env,
		outdir=outdir,
		steps=steps,
		eval_n_runs=eval_n_runs,
		eval_interval=eval_interval,
		max_episode_len=timestep_limit
	)
