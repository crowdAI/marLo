from chainerrl.agents import a3c
from chainerrl.agents import PPO
from chainerrl import links
from chainerrl import misc
from chainerrl.optimizers.nonbias_weight_decay import NonbiasWeightDecay
from chainerrl import policies
import chainer

import logging
import sys
import argparse

import gym
from gym.envs.registration import register

import numpy as np
import marlo
from marlo import experiments
import time

# Tweakable parameters, can be turned into args if needed
gpu = 0
steps = 10 ** 6
eval_n_runs = 10
eval_interval = 10000
update_interval = 2048
outdir = 'results'
lr = 3e-4
bound_mean = False
normalize_obs = False
			
class A3CFFSoftmax(chainer.ChainList, a3c.A3CModel):
    """An example of A3C feedforward softmax policy."""
    def __init__(self, ndim_obs, n_actions, hidden_sizes=(200, 200)):
        self.pi = policies.SoftmaxPolicy(
            model=links.MLP(ndim_obs, n_actions, hidden_sizes))
        self.v = links.MLP(ndim_obs, 1, hidden_sizes=hidden_sizes)
        super().__init__(self.pi, self.v)

    def pi_and_v(self, state):
        return self.pi(state), self.v(state)
		

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
	
# Ensure that you have a minecraft-client running with : marlo-server --port 10000
env_name = 'debug-v0'

register(
    id=env_name,
    entry_point='marlo.envs:MinecraftEnv',
    # Make sure mission xml is in the marlo/assets directory.
    kwargs={'mission_file': args.mission_file}
)

env = gym.make(env_name)

resolution = [84, 84]  # [800, 600]
config = {'allowDiscreteMovement': ["move", "turn"], 'videoResolution': resolution, "turn_based": turn_based}

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

timestep_limit = env.spec.tags.get(
        'wrapper_config.TimeLimit.max_episode_steps'
		)
obs_space = env.observation_space
action_space = env.action_space

model = A3CFFSoftmax(obs_space.low.size, action_space.n)

opt = chainer.optimizers.Adam(alpha=lr, eps=1e-5)
opt.setup(model)

# Initialize the agent
agent = PPO(
			model, opt,
            gpu=gpu,
            phi=phi,
            update_interval=update_interval,
            minibatch_size=64, epochs=10,
            clip_eps_vf=None, entropy_coef=0.0,
        )

# Linearly decay the learning rate to zero
def lr_setter(env, agent, value):
	agent.optimizer.alpha = value

lr_decay_hook = experiments.LinearInterpolationHook(
	steps, 3e-4, 0, lr_setter
	)

# Linearly decay the clipping parameter to zero
def clip_eps_setter(env, agent, value):
	agent.clip_eps = value

clip_eps_decay_hook = experiments.LinearInterpolationHook(
	steps, 0.2, 0, clip_eps_setter
	)

# Use GPU if any available
if gpu >= 0:
	chainer.cuda.get_device(gpu).use()
	model.to_gpu(gpu)
	
# Start training/evaluation
experiments.train_agent_with_evaluation(
	agent=agent,
	env=env,
	eval_env=env,
	outdir=outdir,
	steps=steps,
	eval_n_runs=eval_n_runs,
	eval_interval=eval_interval,
	max_episode_len=timestep_limit,
	step_hooks=[
		lr_decay_hook,
		clip_eps_decay_hook,
	],
)

# Draw the computational graph and save it in the output directory.
chainerrl.misc.draw_computational_graph(
	[q_func(np.zeros_like(obs_space.low, dtype=np.float32)[None])],
	os.path.join(outdir, 'model')
	)