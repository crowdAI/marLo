# marLo

**marLo : Multi Agent Reinforcement Learning using [MalmÖ](https://github.com/Microsoft/malmo)**

# Installation
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

# FAQs
* **I get an error about `MALMO_XSD_PATH`, what do I do ?**
```bash
Traceback (most recent call last):
  File "tutorial_6.py", line 267, in <module>
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
RuntimeError: Schema file Mission.xsd not found in folder specified by
MALMO_XSD_PATH environment variable:
```
As the error message suggests, the `MALMO_XSD_PATH` needs to be set to the
`Schemas` folder. **If you are using the
[Conda environment](#install-malmo), the library already
does this for you**. If not, you will have to download the contents of
this folder, and manually set the `MALMO_XSD_PATH` environment variable to
the absolute path of the `Schemas` folder.

# Authors
* S.P. Mohanty (<sharada.mohanty@epfl.ch>)   
* **...you could be next...**
