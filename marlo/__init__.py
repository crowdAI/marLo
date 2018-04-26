from gym.envs.registration import registry, register, make, spec
import os
import json
import logging

logger = logging.getLogger(__name__)

"""
Assume all folders inside the `marlo_mission_specs` directory represents
a mission_spec
"""
mission_specs_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "marlo_mission_specs")

for mission_spec in os.listdir(mission_specs_dir):
    config_path = os.path.join(
                mission_specs_dir,
                mission_spec,
                "config.json"
            )

    mission_spec_path = os.path.join(
                mission_specs_dir,
                mission_spec,
                "mission_spec.xml"
            )

    if os.path.exists(config_path) and os.path.exists(mission_spec_path):
        config = json.loads(open(config_path).read())
        env_name = config["env_name"]
        # Register this as a Gym Environment
        register(
            id='{}'.format(env_name),
            entry_point='marlo.envs.marlo_base_env:MarloBaseEnv',
            kwargs={'marlo_mission_spec': '{}'.format(env_name)},
            tags={'wrapper_config.TimeLimit.max_episode_steps': 1000},
            reward_threshold=10**10,
        )
        # TODO : Set timelimit from MissionSpec

"""
Set MALMO_XSD_PATH for Conda Environments

If none of the special conditions are met, let MalmoPython throw the
regular error
"""
if "MALMO_XSD_PATH" not in os.environ.keys() or \
        os.environ["MALMO_XSD_PATH"] == "":
    if "CONDA_PREFIX" in os.environ.keys():
        tentative_malmo_xsd_path = os.path.join(
                    os.environ["CONDA_PREFIX"],
                    "install",
                    "Schemas",
                    "Mission.xsd"
                    )
        if os.path.exists(tentative_malmo_xsd_path):
            os.environ["MALMO_XSD_PATH"] = os.path.dirname(
                                            tentative_malmo_xsd_path)
