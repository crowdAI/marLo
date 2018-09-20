import os
import json
import base64
import gym
import importlib
from pathlib import Path
import tempfile

import logging
logger = logging.getLogger(__name__)

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
from .constants import JOIN_WHITELISTED_PARAMS, \
    SINGLE_DIRECTION_DISCRETE_MOVEMENTS, MULTIPLE_DIRECTION_DISCRETE_MOVEMENTS
from .utils import register_environments
from .utils import threaded
from .utils import launch_clients


from .crowdai_helpers import is_grading
from .crowdai_helpers import evaluator_join_token
from .crowdai_helpers import CrowdAiNotifier
from .crowdai_helpers import CrowdAIMarloEvents

########################################################################
# Runtime Variables
########################################################################

########################################################################
# Register All environments
########################################################################
MARLO_ENV_PATHS = [
        os.path.join(
            os.path.abspath(str(Path(__file__).parent)),
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
    """Builds a MarLo environment and returns the `join_tokens` for all the 
    agents in the environment.

    :param env_key: a unique identifier for an environment *or* the path 
        to a mission.xml file
    :type env_key: str
    :param params: a game params dictionary
    :type params: dict


    :returns:  A `list` of `str`, containing `join_tokens` for all the individual agents involved in the game

    >>> import marlo
    >>> client_pool = [('127.0.0.1', 10000)]
    >>> join_tokens = marlo.make("MarLo-MazeRunner-v0", 
    ...                           params=dict(
    ...                              client_pool = client_pool,
    ...                              videoResolution = [800, 600]
    ...                           ))
    """
    if Path(env_key).is_file():
        """
            If a real mission file is passed instead
            of an env_key, then build the env
            from the mission_file
        """
        mission_file = env_key
        params["mission_xml"] = open(mission_file).read()
        env = gym.make("MarLo-RawXMLEnv-v0")
    else:
        env = gym.make(env_key)
    join_tokens = env.init(params, dry_run=True)
    return join_tokens


def init(join_token, params={}):
    """
    Use the provided `join_token` to instantiate a MarLo environment for a single 
    agent.
    
    :param join_token: a token to connect to a marlo game as an agent
    :type join_token: str
    :param params: a game params dictionary
    :type params: dict
    
    >>> import marlo
    >>> client_pool = [('127.0.0.1', 10000)]
    >>> join_tokens = marlo.make("MarLo-MazeRunner-v0", 
    ...                           params=dict(
    ...                              client_pool = client_pool,
    ...                              videoResolution = [800, 600]
    ...                           ))
    >>>
    >>> env = marlo.init(join_tokens[0])
    >>> frame = env.reset()
    """
    join_token = json.loads(
            base64.b64decode(join_token).decode('utf8')
        )

    env = gym.make("MarLo-RawXMLEnv-v0")
    game_params = join_token["game_params"]
    game_params["role"] = join_token["role"]
    game_params["mission_xml"] = join_token["mission_xml"]
    game_params["experiment_id"] = join_token["experiment_id"]
    game_params.update(params)
    env.init(game_params)

    # Notify Evaluation System, if applicable
    CrowdAiNotifier._game_init()
    return env
