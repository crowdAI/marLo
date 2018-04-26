# marLo

**marLo : Multi Agent Reinforcement Learning using [MalmÖ](https://github.com/Microsoft/malmo)**

# Installation
Assuming you have [Anaconda](https://www.anaconda.com/download) installed :
### Env Setup
```bash
conda create python=2.7 --name malmo # you are free to replace '2.7' with python '3.5' or python '3.6'
source activate malmo
conda config --add channels conda-forge
```
### Install malmo
```python
conda install -c crowdai malmo
```
### Check if Malmo is installed properly
```python
python -c "import MalmoPython" #for use of the Python API
malmo-server -port 10001 # For launching the minecraft client
```
### Install marLo
```python
pip install git+https://github.com/spMohanty/marLo
```

# Usage
```python
import marlo
env = marlo.make('marlo-nips2018-env01')
env.init()
observation = env.reset()

for _ in range(1000):
  env.render()
  action = env.action_space.sample() # take a random action
  observation, reward, done, info = env.step(action)
  if done:
    break
```

# Authors
* S.P. Mohanty (<sharada.mohanty@epfl.ch>)   
* **...you could be next...**
