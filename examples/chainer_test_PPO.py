from chainerrl.agents import a3c
from chainerrl.agents import PPO
from chainerrl import experiments
from chainerrl import links
from chainerrl import misc
from chainerrl.optimizers.nonbias_weight_decay import NonbiasWeightDecay
from chainerrl import policies
import chainer
import logging
import sys
import gym
import numpy as np
import marlo
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
	steps, 3e-4, 0, lr_setter)

# Linearly decay the clipping parameter to zero
def clip_eps_setter(env, agent, value):
	agent.clip_eps = value

clip_eps_decay_hook = experiments.LinearInterpolationHook(
	steps, 0.2, 0, clip_eps_setter)

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
