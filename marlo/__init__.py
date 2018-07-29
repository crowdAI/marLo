import os
import json
import base64
import gym
import importlib
from pathlib import Path
import tempfile

try:
    import malmo.MalmoPython as MalmoPython
except ImportError as e:
    err = e
    try:
        import MalmoPython
    except ImportError:
        raise gym.error.DependencyNotInstalled(
                        "{}.\n Malmo doesn't seem to be installed."
                        "Please install Malmo from GitHub or with \n"
                        "> conda install -c crowdai malmo \n"
                        " OR \n"
                        "> pip3 install malmo \n".format(err))


from gym.envs.registration import register
from marlo.base_env_builder import MarloEnvBuilderBase
# Import Constants
from .constants import JOIN_WHITELISTED_PARAMS
from .utils import register_environments

########################################################################
# Register All environments
########################################################################
MARLO_ENV_PATHS = [
        os.path.join(
            os.path.abspath(Path(__file__).parent),
            "envs")
    ]
if os.getenv("MARLO_ENVS_DIRECTORY") is not None:
    # This environment variable expects a list of directories 
    # which contain marlo compatible env definitions
    MARLO_ENV_PATHS += os.getenv("MARLO_ENVS_DIRECTORY").split(":")
register_environments(MARLO_ENV_PATHS)
########################################################################
# Register Envs Complete
########################################################################

def make(env_key, params={}):
    if Path(env_key).is_file():
        """
            If a real mission file is passed instead
            of an env_key, then build the env 
            from the mission_file
        """
        mission_file = env_key
        params["mission_xml"] = open(mission_file).read()
        env = gym.make("RawXMLEnv-v0")
    else:
        env = gym.make(env_key)
    join_tokens = env.init(params)
    return join_tokens


def init(join_token, params={}):
    join_token = json.loads(
            base64.b64decode(join_token).decode('utf8')
        )

    env = gym.make("RawXMLEnv-v0")

    game_params = join_token["game_params"]
    game_params["role"] = join_token["role"]
    game_params["mission_xml"] = join_token["mission_xml"]
    game_params["experiment_id"] = join_token["experiment_id"]
    # game_params.update(params)
    env.init(game_params)
    return env
