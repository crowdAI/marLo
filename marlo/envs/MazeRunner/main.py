#!/usr/bin/env python
from marlo import MarloEnvBuilderBase

import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    def __init__(self):
        super().__init__(
            templates_folder = os.path.join(
                        Path(__file__).parent,
                        "templates"
            )
        )

    @property
    def _default_params(self):
        return dict(
            seed="random",
            tick_length = 50,
            maze_number=0,
            agent_name="MarLo-agent0"
        )

    @property
    def params(self):
        return self._default_params


if __name__ == "__main__":
    env_builder =  MarloEnvBuilder()
    print(env_builder.render())
