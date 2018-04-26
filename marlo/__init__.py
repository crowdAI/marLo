from gym.envs.registration import registry, register, make, spec
import os

register(
    id='marlo-cliff_walking-v01',
    entry_point='gym.envs.algorithmic:CopyEnv',
    tags={'wrapper_config.TimeLimit.max_episode_steps': 1000},
    reward_threshold=10**10,
)

"""
Set MALMO_XSD_PATH for Conda Environments
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
# If none of the special conditions are met, let MalmoPython throw the
# regular error
