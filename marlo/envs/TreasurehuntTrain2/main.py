import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython
import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    """
# Treasure Hunt

## Overview of the game 

Collaborative/Competitive. In an underground dungeon crawling with dangerous enemy entities, teams of players equipped with weapons try to protect their team's collector player, in order for them to safely collect the treasure and reach the exit.

## How to play

* Agents can move forward/backward and turn. Protective players can attack, but cannot collect items. Collector player cannot attack, but can collect items.
* All agents on the team receive 0.25 points if their collector player gets the treasure, and 0.5 points if their collector player reaches the exit (inverse for all other teams, -0.25 and -0.5, respectively).
* All agents on the team receive -1 points if an agent on their team dies (+1 for all other teams).
* The game ends when the collector player reaches the exit (with or without treasures collected), when a player dies or when the time runs out.
* There is a maximum number of steps available (50), and agents get -0.02 point for each step taken.

## Parameters varied for tasks

* Number of enemy entities
* Exit block type
* Treasure & Obstacles (jumps and gaps) block type & count
* Level of protection (armour) for protective players
* Sword & Armour material
* Size of play area
* Number of rooms in dungeon & Distance between rooms
* Time limit 

Game space size: 4.86E+7 
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

