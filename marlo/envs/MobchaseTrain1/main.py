import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython
import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    """
# Mob Chase

## Overview of the game

Collaborative. Two or more Minecraft agents and a mob are wandering a small meadow. The agents have two choices:

- _Catch the mob_ (i.e., the agents pinch or corner the mob(s), and no escape path is available), and receive a high reward (1 point)
- _Give up_ and leave the pen through the exits, marked by special tiles on the edge of the pen, and receive a small reward (0.2 points)

The game is inspired by the variant of the _stag hunt_ presented in [Yoshida et al. 2008]. The [stag hunt](https://en.wikipedia.org/wiki/Stag_hunt) is a classical game theoretic game formulation that captures conflicts between collaboration and individual safety.

[Yoshida et al. 2008] Yoshida, Wako, Ray J. Dolan, and Karl J. Friston. ["Game theory of mind."](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000254) PLoS Comput Biol 4.12 (2008): e1000254.

## How to play

* Agents can move forward/backward and turn. 
* Agents move in turns and try to catch the mob (1 points if caught). 
* Agents can give up on catching the mob in the current round by moving to the "exit squares" on the edge of the play area (0.2 points). 
* There is a maximum number of steps available (50), and agents get -0.02 point for each step taken.

## Parameters varied for tasks

* time = [0, 3000, 6000]
* mob_types = ['Pig', 'Cow', 'Chicken']
* exit_blocks = ['diamond_block', 'brick_block', 'purpur_block', 'bone_block', 'emerald_block']
* edge_blocks = ['fence', 'spruce_fence', 'jungle_fence', 'dark_oak_fence']
* edge_ground = ['sand', 'clay', 'water']
* mob_count = [1, 2]
* grid_size = [9, 11]
* exit_block_counts = [2, 3, 4]
* obstacle_counts = [2, 4, 6]

Game design space size: 1.94E+4


"""
    
    def __init__(self, extra_params=None):
        if extra_params is None:
            extra_params={}
        super(MarloEnvBuilder, self).__init__(
                templates_folder=os.path.join(
                            str(Path(__file__).parent),
                            "templates"
                )
        )
        self.params = self._default_params()
        # You can do something with the extra_params if you wish

    def _default_params(self):
        _default_params = super(MarloEnvBuilder, self).default_base_params
        return _default_params


if __name__ == "__main__":
    env_builder = MarloEnvBuilder()
    mission_xml = env_builder.render_mission_spec()
    mission_spec = MalmoPython.MissionSpec(mission_xml, True)
    print(mission_spec.getSummary())

