# Marlo

**marLo : Multi Agent Reinforcement Learning using [MalmÖ](https://github.com/Microsoft/malmo)**

**NOTE : THIS IS A WORK IN PROGRESS. AND NOT READY FOR THE FIRST RELEASE YET**

Marlo requires Python3 and Java8 to be installed. On Windows Python3 MUST be the 64bit version.

### Install malmo

```bash
pip3 install malmo
```

### Alternatively install malmo from GitHub

If the above fails then you may need to install malmo manually:
Please see [Malmo GitHub](https://github.com/Microsoft/malmo) on how to install Malmo from a binary release or building from source.
On Linux and MacOS, You will need to include the MalmoPython.so library on your PYTHONPATH.
Mincraft can then be launched from the malmo/Minecraft directory using the launchClient.sh or launchClient.bat script with the -port argument specifying the port.

### Install marlo from GitHub

```
git clone https://github.com/spMohanty/marlo
cd marlo
python setup.py install
```

## Running the multi agent examples

The multi-agent examples can be run from the marlo directory.

Assuming malmo was installed with pip, you can start Minecraft on ports 1000 and 10001 
by running the following in a cmd terminal or shell:

```
python3 two_agent_minecraft_launch.py 
```

Once two minecraft windows appear, run the multi agent example with:

```
python3 -m examples.multiagentexample --turn_based --rollouts 10  --mission_file mob_chase.xml
```
or for the full Chainer RL experience:

```
python3 -m examples.multiagent_chainer_test_DQN --turn_based --rollouts 10  --mission_file mob_chase.xml
```
