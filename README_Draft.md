## --- This is a draft document ---

## Introduction
Marlo (short for Multi-Agent Reinforcement Learning in Malmo) is an artificial intelligence competition primarily aimed towards the goal of implementing reinforcement learning agents with a great degree of generality, capable of solving problems in pseudo-random, procedurally changing multi-agent environments within the world of the mediatic phenomenon game Minecraft.

Marlo is based off of the [Malmo](https://github.com/Microsoft/malmo) framework, which is a platform for Artificial Intelligence experimentation and research built on top of Minecraft. The Malmo platform provides a high-level API which enables access to actions, observations (i.e. location, surroundings, video frames, game statistics) and other general data that Minecraft provides. Marlo, on the other hand, is a wrapper for Malmo that provides a more standardized RL-friendly environment for scientific study.

The framework is written as an extension to [OpenAI's Gym](https://github.com/openai/gym) framework, which is a toolkit for developing and comparing reinforcement learning algorithms, thus providing an industry-standard and familiar platform for scientists, developers and popular RL frameworks.

Due to the framework's nature as an wrapper for Malmo, a few steps must be taken in order to be able to boot up and run Marlo.

## Getting started
### Marlo installation with Malmo repack
1. Install a suitable version of Malmo
    * This can easily be done by following the step-by-step guide that Malmo provides for [Windows](https://github.com/Microsoft/malmo/blob/master/doc/install_windows.md), [Linux](https://github.com/Microsoft/malmo/blob/master/doc/install_linux.md), [MacOSX](https://github.com/Microsoft/malmo/blob/master/doc/install_macosx.md).
    * *Please make sure to download a pre-compiled version of Malmo as posted on the release page as doing this is ***not*** the same as downloading the GitHub repository ZIP file. If you choose to download the repository, you will have to ***build the package yourself*** which is a lengthier process. If you get errors along the lines of "ImportError: No module named MalmoPython" it will probably be because you have made this mistake.*
    * Please ensure that all the redistributables that Malmo requires are installed correctly, and that the following entries appear as environment variables:
        * MALMO_XSD_PATH = Malmo_dir\Schemas folder
        * JAVA_HOME = jdk installation folder
2. Clone Marlo repository from [this](https://github.com/spMohanty/marLo/tree/dev) GitHub repository's Master branch.
3. Navigate to the folder where you have downloaded the repository and run the setup.py file: *python setup.py install*
    * This should install all the required packages for Marlo to function.
    * In some special circumstances, some packages might fail to install, prompting you to install them yourself. When this happens, the error message usually contains the name and link to the missing packages which you should install using PyPi.
    * Note: if an import error describing a missing "scoretable" class appears, please downgrade Gym to version 0.7.4 like such: *pip install -U gym==0.7.4*

### Marlo installation with Malmo as PyPi wheel
Assuming you have [Anaconda](https://www.anaconda.com/download) installed :
### Env Setup
```bash
conda create python=3.6 --name malmo
# you are free to replace '3.6' with python '3.5' or python '2.7'.
# Though only python 3.* versions will be officially supported.
source activate malmo
conda config --add channels conda-forge
```

### Install malmo
```python
conda install -c crowdai malmo
conda install gcc psutil
pip install pygame
```
### Check if Malmo is installed properly
```python
python -c "import MalmoPython" #for use of the Python API
$MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000 # For launching the minecraft client (TODO: Fix name conventions)
# Or if you are not using the conda package, then you are free to launch the minecraft client
# using your method of choice.

# This might take a few seconds on the first execution. So hang in there.
```

### Install marLo
 ```
git clone -b dev https://github.com/spMohanty/marlo
cd marlo
python setup.py install
```

## Running

*Note*: Ensure that you have the env directory `MALMO_XSD_PATH` pointing to the correct Schemas folder.
If you are using the conda package for malmo, then you can do a :
`export MALMO_XSD_PATH=$CONDA_PREFIX/install/Schemas`.   

Also do ensure that you have a minecraft-client running on port `10000`.

```python
import gym
import marlo

env = gym.make('MinecraftBasic-v0')
env.init(
    allowContinuousMovement=["move", "turn"],
    videoResolution=[800, 600]
    )
env.reset()

done = False
while not done:
        env.render()
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        print(action)

env.close()
```

## Available Options
More documentation about configuration options is in [docs/init.md](docs/init.md).


### Marlo installation with self-compiled Malmo
If you have taken the time to compile Malmo on your own, then chances are this step is unneeded. Simply clone Marlo from the [GitHub repository](https://github.com/spMohanty/marLo/tree/dev) and run the setup file via *python setup.py install*.

## Using our recommended framework, ChainerRL
In their own words, Chainer "is a Python-based deep learning framework aiming at flexibility". It has a very powerful high-level API aimed at training deep learning networks and as such is very useful in a RL context. ChainerRL is a deep reinforcement learning library that implements various state-of-the-art deep reinforcement algorithms in Python using Chainer.

ChainerRL is the Marlo's officially endorsed framework and as such examples for its usage will be posted: however, ChainerRL is by no means mandatory for the competition!

The framework presents a wide range of algorithms and deep learning tools which facilitate a quick start-up and as such is ideal for drafts. ChainerRL communicates seamlessly with OpenAI's Gym framework, thus relieving a lot of structural stress off of you - the competitor - and allowing you to focus strictly on your agent's behaviour.

### Installing and running ChainerRL
Please refer to ChainerRL's [official GitHub](https://github.com/chainer/chainerrl) for installation instructions and further documentation. Alternatively, you can simply use PyPi to download and install ChainerRL as a package via the following command: *pip install chainerrl*. Following this, you can simply proceed to testing it out via following the steps laid out in ChainerRL's official [getting started guide](https://github.com/chainer/chainerrl/blob/master/examples/quickstart/quickstart.ipynb).

### Integration with Marlo
As described previously, ChainerRL interacts with Marlo seamlessly. Let us take the implementation of a PPO agent in Minecraft using ChainerRL and Marlo and break it down into simpler steps.

First it is necessary to start up a Minecraft client on port 10000 such that Marlo can use it. This is very easy to do if you have followed the previous steps and have therefore installed a repacked version of Malmo, since it comes already packed with a Minecraft launcher. Simply navigate to your Malmo folder with your favorite CLI and then:
```cmd
cd Minecraft
.\launchClient.bat
```
or
```sh
cd Minecraft
.\launchClient.sh
```
If this is your first time running Malmo, please be patient as building the Gradle client takes a while. Don't worry if the console shows 95% completion as long as the game runs: the server is running and agents will work.

In case you've installed Malmo as a PyPi wheel, you can use the following command:
```cmd
python3 -c 'import malmo.minecraftbootstrap; malmo.minecraftbootstrap.launch_minecraft()'
```

You are now ready to start putting together your ChainerRL PPO!

#### Imports and variables
Let us first import PPO, its subsidiary A3C, as well as other chainer and chainerRL-related classes. We will also import numpy and marlo as these will be used later.

```python3
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
gpu = 1
steps = 10 ** 6
eval_n_runs = 10
eval_interval = 10000
update_interval = 2048
outdir = 'results'
lr = 3e-4
bound_mean = False
normalize_obs = False
```
#### Declaring a policy
We will use the A3C feedforward softmax policy, and this will be implemented in a standard fashion as below:
```python3
class A3CFFSoftmax(chainer.ChainList, a3c.A3CModel):
    """An example of A3C feedforward softmax policy."""
    def __init__(self, ndim_obs, n_actions, hidden_sizes=(200, 200)):
        self.pi = policies.SoftmaxPolicy(
            model=links.MLP(ndim_obs, n_actions, hidden_sizes))
        self.v = links.MLP(ndim_obs, 1, hidden_sizes=hidden_sizes)
        super().__init__(self.pi, self.v)

    def pi_and_v(self, state):
        return self.pi(state), self.v(state)
```

#### Creating the environment
First, let us create a phi function that transforms items to float32 (since ChaineRL uses float32, but Gym uses float64!)
```python3
def phi(obs):
    return obs.astype(np.float32)
```

With that out of the way, let us create the environment in a typical Gym fashion.
```python3
# Ensure that you have a minecraft-client running with : marlo-server --port 10000
env = gym.make('MinecraftCliffWalking1-v0')

env.init(
    allowContinuousMovement=["move", "turn"],
    videoResolution=[800, 600]
    )
```

Marlo environments support a wide range of initialization parameters, as seen [here](https://github.com/spMohanty/marLo/blob/dev/docs/init.md). You can use any of these in the *env_init()* function.

Currently, the number of available environments is limited and their string titles can all be found [here](https://github.com/spMohanty/marLo/blob/dev/docs/available_envs.md). Feel free to swap any of these in the *gym.make("")* call at the beginning of the file in order to select a different mission to train on.

 Finally, let us render the environment and print out some helpful statistics.
```python3
obs = env.reset()
env.render()
print('initial observation:', obs)

action = env.action_space.sample()
obs, r, done, info = env.step(action)
print('next observation:', obs)
print('reward:', r)
print('done:', done)
print('info:', info)

print('actions:', str(env.action_space))
```
The print comments are there solely for debugging reasons, they tend to be rather helpful when something goes wrong whilst trying to kick an environment off.

#### Initialize the agent
In order to create a PPO agent, we must initialize it. ChainerRL's PPO agent class requires a model parameter, which is represented here by our chosen softmax policy. Therefore, we need to instantiate our policy for use in the agent:
```python3
timestep_limit = env.spec.tags.get(
        'wrapper_config.TimeLimit.max_episode_steps'
		)
obs_space = env.observation_space
action_space = env.action_space

model = A3CFFSoftmax(obs_space.low.size, action_space.n)
```

We should also use an optimizer for the policy. In this case we're using the [Adam algorithm](https://machinelearningmastery.com/adam-optimization-algorithm-for-deep-learning/):
```python3
opt = chainer.optimizers.Adam(alpha=lr, eps=1e-5)
opt.setup(model)
```

Finally, we initialize PPO with the policy, optimizer and pre-set variables as declared at the top of the file.
```python3
# Initialize the agent
agent = PPO(
            model, opt,
            gpu=gpu,
            phi=phi,
            update_interval=update_interval,
            minibatch_size=64, epochs=10,
            clip_eps_vf=None, entropy_coef=0.0,
        )
 ```

 #### Decay the learning and cliping rate linearly
 This step is simply used as part of the implementation of PPO, which supposes a linear decay for the learning rate towards zero:
 ```python3
 # Linearly decay the learning rate to zero
def lr_setter(env, agent, value):
	agent.optimizer.alpha = value

lr_decay_hook = experiments.LinearInterpolationHook(
	steps, 3e-4, 0, lr_setter)
 ```
 and a linear decay of the clipping rate towards zero:
 ```python3
 # Linearly decay the clipping parameter to zero
def clip_eps_setter(env, agent, value):
	agent.clip_eps = value

clip_eps_decay_hook = experiments.LinearInterpolationHook(
	steps, 0.2, 0, clip_eps_setter)
 ```
 #### Start training!
 We should loop over the number of episodes and timesteps as initialized at the beginning of this file whilst calling the *act()* method of the PPO as we go, which can be rather cumbersome. Fortunately, ChainerRL provides an easy way to do this via its [experiments pack](https://github.com/chainer/chainerrl/tree/master/chainerrl/experiments). Let us call the *train_agent_with_evaluation()* function on our PPO:
 ```python3
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
```

Et voila! Your agent is now ready to start aggressively walking towards walls for weeks on end as it finds its way through the complex jungle that Minecraft gameplay is!
