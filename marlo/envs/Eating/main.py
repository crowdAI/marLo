#!/usr/bin/env python
import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython


import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    """
    Description: 
		This environment is a flat map littered with lots of food items which the agent can
		pick up. The goal is to pick up only healthy foods - the agent is thus prompted to
		prefer certains items over others.
		
	Actions available:
		Move forward/backward
		Jump
		Turn
		Strafe
		Crouch
		Use
		
	Rewards:
		2 points for picking up: fish, porkchop, beef, chicken, rabbit, mutton
        1 point for picking up: potato, egg, carrot
        -1 points for picking up: apple, melon
        -2 points for picking up: sugar, cake, cookie, pumpkin pie
    
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
