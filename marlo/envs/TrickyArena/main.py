#!/usr/bin/env python
import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython


import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    """
    Description: 
		The layout of this mission is that of a flat map littered with
		redstone, obsidian and ice blocks, as well as water and lava holes.
		The goal of the agent is to step on as many obsidian blocks
		as possible before heading towards a redstone block, at which
		point the mission ends.
		
	Actions available:
		Jump
		Move
		Pitch
		Strafe
		Turn
		Crouch
		Use
		
	Rewards:
		100 points with a 1 second delay for each obsidian block touched
		-1000 points upon death
		-900 points for running out of time
		100 points for leaving the arena (touching stained glass)
		-800 points for falling in a water hole
		400 points for finding a redstone block
		
    """
	   
    def __init__(self, extra_params={}):
        super(MarloEnvBuilder, self).__init__(
                templates_folder = os.path.join(
                            str(Path(__file__).parent),
                            "templates"
                )
        )
        self.params = self._default_params()
        # You can do something with the extra_params if you wish
        self.params.update(extra_params)

    def _default_params(self):
        _default_params = super(MarloEnvBuilder, self).default_base_params
        _default_params.update(
            dict(
                tick_length=50,
                agent_names=["MarLo-agent0"],
            )
        )
        return _default_params


if __name__ == "__main__":
    env_builder =  MarloEnvBuilder()
    print(env_builder.params)
    print(env_builder.params.experiment_id)
    mission_xml = env_builder.render_mission_spec()
    mission_spec = MalmoPython.MissionSpec(mission_xml, True)
    print(mission_spec.getSummary())
