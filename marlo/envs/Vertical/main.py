#!/usr/bin/env python
import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython


import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    """    
    Description: 
		This is a map with many vertical emplacements such as stairs or ladders.
		The agent's task is to find the gold/diamond/redstone block at the top of the tower
		by climbing the stairs/ladders suitably.
		
	Actions available:
		Jump
		Move
		Pitch
		Strafe
		Turn
		Crouch
		Use
		
	Rewards:
		8000 points for finding the goal
		-1000 points for running out of time
		20 points for finding a gold/diamond/redstone ore
    """
    def __init__(self, extra_params={}):
        super(MarloEnvBuilder, self).__init__(
                templates_folder = os.path.join(
                            Path(__file__).parent,
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
                tick_length=10,
                agent_names=["MarLo-agent0"],
                episode_timelimit=60000
            )
        )
        return _default_params

    def render_mission_spec(self):
        """
        TODO: Randomize  location of food items
        """
        template = self.jinj2_env.get_template("mission.xml")
        return template.render(
            params=self.params
        )


if __name__ == "__main__":
    env_builder =  MarloEnvBuilder()
    print(env_builder.params)
    print(env_builder.params.experiment_id)
    mission_xml = env_builder.render_mission_spec()
    mission_spec = MalmoPython.MissionSpec(mission_xml, True)
    print(mission_spec.getSummary())
