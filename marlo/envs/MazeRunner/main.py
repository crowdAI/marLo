#!/usr/bin/env python
from marlo import MalmoPython, MarloEnvBuilderBase

import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    def __init__(self):
        super(MarloEnvBuilder, self).__init__(
                templates_folder = os.path.join(
                            Path(__file__).parent,
                            "templates"
                )
        )

    @property
    def _default_params(self):
        _default_params = super(MarloEnvBuilder, self).default_base_params
        _default_params.update(
            dict(
                seed="random",
                tick_length = 50,
                agent_name="MarLo-agent0"
            )
        )
        return _default_params

    @property
    def params(self):
        return self._default_params


if __name__ == "__main__":
    env_builder =  MarloEnvBuilder()
    print(env_builder.params)
    print(env_builder.params.experiment_id)
    mission_xml = env_builder.render_mission_spec()
    mission_spec = MalmoPython.MissionSpec(mission_xml, True)
    print(mission_spec.getSummary())
