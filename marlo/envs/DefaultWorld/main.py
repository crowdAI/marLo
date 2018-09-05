#!/usr/bin/env python
import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython


import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    """
    Description: 
		This environment thrusts the agent into a normal, random Minecraft world. The seed is
		generated randomly, therefore the location is not always the same. The goal is to find
		a gold/diamond/redstone block in time. 
		
	Actions available:
		Forward/Backward
		Turning
		
	Rewards:
		1000 points for finding the goal
		-1000 points for running out of time
		-10000 points for death
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
                reward_death=-10000,
                reward_found_goal=1000,
                reward_out_of_time=-1000
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
