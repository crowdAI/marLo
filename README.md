# Marlo

**marLo : Multi Agent Reinforcement Learning using [MalmÖ](https://github.com/Microsoft/malmo)**

**NOTE : THIS IS A WORK IN PROGRESS. AND NOT READY FOR THE FIRST RELEASE YET**


List of task :  [MalmoMissionTable_CurrentTasks_2016_06_14.pdf](https://github.com/Microsoft/malmo/raw/master/sample_missions/MalmoMissionTable_CurrentTasks_2016_06_14.pdf).

## Installation

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
malmo-server -port 10000 # For launching the minecraft client (TODO: Fix name conventions)
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

## Available Envs
List of all available envs can be found [available_envs.md](docs/available_envs.md)

## Available Options

More documentation about configuration options is in [docs/init.md](docs/init.md).


# Author
Sharada Mohanty (sharada.mohanty@epfl.ch)
