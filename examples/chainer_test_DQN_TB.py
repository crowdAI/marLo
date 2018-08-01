from chainerrl.agents.dqn import DQN
from chainerrl import experiments
from chainerrl import explorers
from chainerrl import links
from chainerrl import misc
from chainerrl import q_functions
from chainerrl import replay_buffer
from chainer import optimizers
import chainerrl
import logging
import sys, os

import gym
gym.undo_logger_setup()  # NOQA
from gym import spaces
import gym.wrappers

import numpy as np
import marlo
import time

from tb_chainer import name_scope, within_name_scope

class QFunction(chainer.Chain):

    def __init__(self, obs_size, n_actions, n_hidden_channels=50):
        super().__init__()
        with self.init_scope():
            self.l0 = L.Linear(obs_size, n_hidden_channels)
            self.l1 = L.Linear(n_hidden_channels, n_hidden_channels)
            self.l2 = L.Linear(n_hidden_channels, n_actions)

	@within_name_scope('MLP')
    def __call__(self, x, test=False):
        """
        Args:
            x (ndarray or chainer.Variable): An observation
            test (bool): a flag indicating whether it is in test mode
        """
		with name_scope('linear1', self.l0.params()):
			h1 = F.tanh(self.l0(x))
		with name_scope('linear2', self.l1.params()):
			h2 = F.tanh(self.l1(h1))
		with name_scope('linear3', self.l2.params()):
            o = self.l2(h2)
			
        return chainerrl.action_value.DiscreteActionValue(o)

# Tweakable parameters
n_hidden_channels = 100
n_hidden_layers = 2
start_epsilon = 1.0
end_epsilon = 0.1
final_exploration_steps = 10 ** 4
outdir = 'results'
gpu = None
gamma = 0.99
replay_start_size = 1000
target_update_interval = 10 ** 2
update_interval = 1
target_update_method = 'hard'
soft_update_tau = 1e-2
rbuf_capacity = 5 * 10 ** 5
steps = 10 ** 5
eval_n_runs = 100
eval_interval = 10 ** 4

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
print('sample action:', str(env.action_space.sample))

timestep_limit = env.spec.tags.get('wrapper_config.TimeLimit.max_episode_steps')
obs_space = env.observation_space
obs_size = obs_space.low.size
action_space = env.action_space

n_actions = action_space.n

#q_func = q_functions.FCStateQFunctionWithDiscreteAction(
			#obs_size, n_actions,
			#n_hidden_channels=n_hidden_channels,
			#n_hidden_layers=n_hidden_layers
		#)
	
q_func = QFunction(
			obs_size, n_actions,
		)
		
# Use epsilon-greedy for exploration
# Constant
explorer = explorers.ConstantEpsilonGreedy(
			epsilon = 0.3, 
			random_action_func=env.action_space.sample
		)
		
# Linear decay
#explorer = explorers.LinearDecayEpsilonGreedy(
			#start_epsilon, 
			#end_epsilon, 
			#final_exploration_steps,
			#random_action_func=str(env.action_space.sample)
		#)

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

	
# Start tensorboard writer
writer = SummaryWriter('runs/'+datetime.now().strftime('%B%d  %H:%M:%S'))

# Start training
experiments.train_agent_with_evaluation(
		agent=agent, 
		env=env, 
		eval_env=env,
		steps=steps,
		eval_n_runs=eval_n_runs, 
		eval_interval=eval_interval,
		outdir=outdir, 
		max_episode_len=timestep_limit
	)
	
# Draw the computational graph and save it in the output directory.
chainerrl.misc.draw_computational_graph(
	[q_func(np.zeros_like(obs_space.low, dtype=np.float32)[None])],
	os.path.join(outdir, 'model')
	)
