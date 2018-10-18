import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython
import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    """
# Build Battle

## Overview of the game

Collaborative/Competitive. Two teams of agents compete to build a given cuboid structure within a time limit.

## How to play

* Agents can move forward/backward, turn, jump, attack or destroy objects.
* Agents move in turns and try to copy the given structure.
* The reward scale is .2 (+.2 for placing correct block / removing incorrect block; -.2 for placing incorrect block / removing correct block).
* Agents receive the scaled rewards in the following distribution: 0.2 for agent, 0.1 for teammate, -0.1 for opponent.
* There is a time limit proportional to the number of blocks missing from the structure to be built by players. The game ends when the time limit is reached or when the structure is complete. Agents receive +1 points for completing the structure.
* There is a maximum number of steps available (50), and agents get -0.02 point for each step taken.

## Parameters varied for tasks

* block_types = ['lapis_block', 'diamond_block', 'brick_block', 'coal_block', 'purpur_block', 'stone']
* cuboid_dimension_x = [1, 2, 3]
* cuboid_dimension_y = [1, 2, 3]
* cuboid_dimension_z = [1, 2, 3]
* distance_structures_x = [3, 4]
* distance_structures_z = [0, 1, 2]
* percent_structure_built = [20 - 80] (min. 1 built + 1 missing)

Game design space size: 1.73E+4
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

