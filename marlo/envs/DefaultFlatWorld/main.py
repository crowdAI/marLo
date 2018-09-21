#!/usr/bin/env python
import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython


import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    """
    Description: 
		This is a simple, plain map, in which the sole goal is to reach a location nearby
		the spawn of the agent. The weather is dark and snowy, but that aside there is not
		much to describe in relation to this mission.
		
	Actions available:
		Forward/Backward
		Turning
		
	Rewards:
		100 points for reaching the location
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
