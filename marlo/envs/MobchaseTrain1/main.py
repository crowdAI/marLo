import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython
import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    """Chase the Mobs
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

