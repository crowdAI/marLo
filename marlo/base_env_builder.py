#!/usr/bin/env python
import time
import gym
import numpy as np
import marlo
from marlo import MalmoPython

import traceback

from jinja2 import Environment as jinja2Environment
from jinja2 import FileSystemLoader as jinja2FileSystemLoader

import logging
logger = logging.getLogger(__name__)


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class MarloEnvBuilderBase(gym.Env):
    """
    Base class for all Marlo environment builders
    """
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, templates_folder):
        super(MarloEnvBuilderBase, self).__init__()
        self.templates_folder = templates_folder
        self.setup_templating()
        self._default_base_params = False

        self.agent_host = MalmoPython.AgentHost()
        self.mission_spec = None
        self.client_pool = None
        self.experiment_id = "experiment_id"

    def setup_templating(self):
        self.jinja2_fileloader = jinja2FileSystemLoader(self.templates_folder)
        self.jinj2_env = jinja2Environment(loader=self.jinja2_fileloader)

    def render_mission_spec(self):
        template = self.jinj2_env.get_template("mission.xml")
        return template.render(
            params=self.params
        )

    @property
    def white_listed_join_params(self):
        return [
            "videoResolution",
            "recordMP4"
        ]

    @property
    def default_base_params(self):
        if not self._default_base_params:
            self._default_base_params = dotdict(
                 seed="random",
                 role=0,
                 experiment_id="something",
                 client_pool = None,
                 continuous_discrete=True,
                 add_noop_command=None,
                 max_retries=30,
                 retry_sleep=3,
                 step_sleep=0.001,
                 skip_steps=0,
                 videoResolution=[800, 600],
                 videoWithDepth=None,
                 observeRecentCommands=None,
                 observeHotBar=None,
                 observeFullInventory=None,
                 observeGrid=None,
                 observeDistance=None,
                 observeChat=None,
                 allowContinuousMovement=None,
                 allowDiscreteMovement=None,
                 allowAbsoluteMovement=None,
                 recordDestination=None,
                 recordObservations=None,
                 recordRewards=None,
                 recordCommands=None,
                 recordMP4=None,
                 gameMode=None,
                 forceWorldReset=None,
                 turn_based=False,
            )
        return self._default_base_params

    def setup_video(self, params):
        ############################################################
        # Setup Video
        ############################################################        
        if params.videoResolution:
            if params.videoWithDepth:
                self.mission_spec.requestVideoWithDepth(
                    *params.videoResolution
                    )
            else:
                self.mission_spec.requestVideo(*params.videoResolution)

    def setup_observe_params(self, params):
        ############################################################
        # Setup observe<>*
        ############################################################
        if params.observeRecentCommands:
            self.mission_spec.observeRecentCommands()
        if params.observeHotBar:
            self.mission_spec.observeHotBar()
        if params.observeFullInventory:
            self.mission_spec.observeFullInventory()
        if params.observeGrid:
            self.mission_spec.observeGrid(*(params.observeGrid + ["grid"]))
        if params.observeDistance:
            self.mission_spec.observeDistance(
                *(params.observeDistance + ["dist"])
                )
        if params.observeChat:
            self.mission_spec.observeChat()

    def setup_action_commands(self, params):
        ############################################################
        # Setup Action Commands
        ############################################################
        if params.allowContinuousMovement or params.allowAbsoluteMovement or \
                params.allowDiscreteMovement:
            # Remove all command handlers
            self.mission_spec.removeAllCommandHandlers()

            # ContinousMovement commands
            if isinstance(params.allowContinuousMovement, list):
                for _command in params.allowContinuousMovement:
                    self.mission_spec.allowContinuousMovementCommand(_command)
            elif params.allowContinuousMovement is True:
                self.mission_spec.allowAllContinuousMovementCommands()

            # AbsoluteMovement commands
            if isinstance(params.allowAbsoluteMovement, list):
                for _command in params.allowAbsoluteMovement:
                    self.mission_spec.allowAbsoluteMovementCommand(_command)
            elif params.allowAbsoluteMovement is True:
                self.mission_spec.allowAllAbsoluteMovementCommands()

            # DiscreteMovement commands
            if isinstance(params.allowDiscreteMovement, list):
                for _command in params.allowDiscreteMovement:
                    self.mission_spec.allowDiscreteMovementCommand(_command)
            elif params.allowDiscreteMovement is True:
                self.mission_spec.allowAllDiscreteMovementCommands()

    def setup_observation_space(self, params):
        ############################################################
        # Setup Observation Space
        ############################################################
        self.video_height = self.mission_spec.getVideoHeight(0)
        self.video_width = self.mission_spec.getVideoWidth(0)
        self.video_depth = self.mission_spec.getVideoChannels(0)
        self.observation_space = gym.spaces.Box(
                low=0, high=255,
                shape=(self.video_height, self.video_width, self.video_depth),
                dtype=np.uint8
                )
        # Setup a dummy first image
        self.last_image = np.zeros(
            (self.video_height, self.video_width, self.video_depth),
            dtype=np.uint8
            )

    def setup_action_space(self, params):
        ############################################################
        # Setup Action Space
        ############################################################
        SINGLE_DIRECTION_DISCRETE_MOVEMENTS = \
                    [
                        "jumpeast", "jumpnorth", "jumpsouth", "jumpwest",
                        "movenorth", "moveeast", "movesouth", "movewest",
                        "jumpuse", "use", "attack", "jump"
                    ]
        MULTIPLE_DIRECTION_DISCRETE_MOVEMENTS = \
                    [
                        "move", "turn", "look", "strafe", "jumpmove", 
                        "jumpstrafe"
                    ]

        continuous_actions = []
        discrete_actions = []
        multidiscrete_actions = []
        multidiscrete_action_ranges = []
        if params.add_noop_command:
            discrete_actions.append("move 0\nturn 0")
        command_handlers = self.mission_spec.getListOfCommandHandlers(0)
        for command_handler in command_handlers:
            commands = self.mission_spec.getAllowedCommands(0, command_handler)
            for command in commands:
                logger.debug("Command : {}".format(command))
                if command_handler == "ContinuousMovement":
                    if command in ["move", "strafe", "pitch", "turn"]:
                        if params.continuous_discrete:
                            discrete_actions.append(command + " 1")
                            discrete_actions.append(command + " -1")
                        else:
                            continuous_actions.append(command)
                    elif command in ["crouch", "jump", "attack", "use"]:
                        if params.continuous_discrete:
                            discrete_actions.append(command + " 1")
                            discrete_actions.append(command + " 0")
                        else:
                            multidiscrete_actions.append(command)
                            multidiscrete_action_ranges.append([0, 1])
                    else:
                        raise ValueError(
                            "Unknown continuois action : {}".format(command)
                            )
                elif command_handler == "DiscreteMovement":
                    if command in SINGLE_DIRECTION_DISCRETE_MOVEMENTS:
                        discrete_actions.append(command + " 1")
                    elif command in MULTIPLE_DIRECTION_DISCRETE_MOVEMENTS:
                        discrete_actions.append(command + " 1")
                        discrete_actions.append(command + " -1")
                    else:
                        raise ValueError(
                            "Unknown discrete action : {}".format(command)
                        )
                elif command_handler in ["AbsoluteMovement", "Inventory"]:
                    raise NotImplementedError(
                        "Command Handler `{}` Not Implemented".format(
                            command_handler
                        )
                    )
                else:
                    raise ValueError(
                        "Unknown Command Handler : `{}`".format(
                            command_handler
                            )
                    )
        # Convert lists into proper gym action spaces
        self.action_names = []
        self.action_spaces = []

        # Discrete Actions
        if len(discrete_actions) > 0:
            self.action_spaces.append(
                gym.spaces.Discrete(len(discrete_actions))
                )
            self.action_names.append(discrete_actions)
        # Continuous Actions
        if len(continuous_actions) > 0:
            self.action_spaces.append(
                gym.spaces.Box(-1, 1, (len(continuous_actions),))
                )
            self.action_names.append(continuous_actions)
        if len(multidiscrete_actions) > 0:
            self.action_spaces.append(
                gym.spaces.MultiDiscrete(multidiscrete_action_ranges)
                )
            self.action_names.append(multidiscrete_actions)

        # No tuples in case a single action
        if len(self.action_spaces) == 1:
            self.action_space = self.action_spaces[0]
        else:
            self.action_space = gym.spaces.Tuple(self.action_space)

    def setup_client_pool(self, params):
        ############################################################
        # Setup Client Pool
        ############################################################
        if params.client_pool:
            self.client_pool = MalmoPython.ClientPool()
            for _client in params.client_pool:
                self.client_pool.add(MalmoPython.ClientInfo(*_client))

            if not isinstance(params.client_pool, list):
                raise ValueError("params.client_pool must be a list of tuples"
                                 "of (ip_address, port)")

    def setup_mission_record(self, params):
        ############################################################
        # Setup Mission Record
        ############################################################
        self.mission_record_spec = MalmoPython.MissionRecordSpec() # empty
        if params.recordDestination:
            self.mission_record_spec.setDestination(params.recordDestination)
        if params.recordRewards:
            self.mission_record_spec.recordRewards()
        if params.recordCommands:
            self.mission_record_spec.recordCommands()
        if params.recordMP4:
            self.mission_record_spec.recordMP4(*params.recordMP4)

    def setup_game_mode(self, params):
        ############################################################
        # Setup Game Mode
        ############################################################
        if params.gameMode:
            if params.gameMode == "spectator":
                self.mission_spec.setModeToSpectator()
            elif params.gameMode == "creative":
                self.mission_spec.setModeToCreative()
            elif params.gameMode == "survival":
                logger.info("params.gameMode : Cannot force survival mode.")
            else:
                raise Exception("Unknown params.gameMode : {}".format(
                    params.gameMode
                ))

    def init(self, params):
        #TODO: Filter unwanted params here in case of join
        # for _key in params:
        #     if _key not in marlo.JOIN_WHITELISTED_PARAMS:
        #         del params[_key]
                
        self.params.update(params)
        return self.build_env(self.params)
    
    def build_env(self, params):
        ############################################################
        # Instantiate Mission Spec
        ############################################################
        mission_xml = self.render_mission_spec()
        self.mission_spec = MalmoPython.MissionSpec(mission_xml, True)

        self.setup_video(params)
        self.setup_observe_params(params)
        self.setup_action_commands(params)
        self.setup_observation_space(params)
        self.setup_action_space(params)
        self.setup_client_pool(params)

        self.setup_mission_record(params)
        self.setup_game_mode(params)

    ########################################################################
    # Env interaction functions
    ########################################################################
    def step(self, action):
        return True

    def reset(self):
        if self.params.forceWorldReset:
            # Force a World Reset on each reset
            self.mission_spec.forceWorldReset()

        # Attempt to start a mission
        for retry in range(self.params.max_retries + 1):
            print("RETRY : {}".format(retry))
            # Role 0 (the server) could take some extra time to start
            if self.params.role != 0:
                time.sleep(1)
            else:
                time.sleep(0.1)
            try:
                print("Client Pool : ", self.client_pool)
                if self.client_pool:
                    self.agent_host.startMission(
                        self.mission_spec,
                        self.client_pool,
                        self.mission_record_spec,
                        self.params.role,
                        self.experiment_id
                    )
                else:
                    self.agent_host.startMission(
                        self.mission_spec, 
                        self.mission_record_spec
                        )
                break #Break out of the try-to-connect loop
            except RuntimeError as e:
                traceback.format_exc()
                if retry == self.params.max_retries:
                    logger.error("Error Starting Mission : {}".format(
                        traceback.format_exc()
                    ))
                    raise e
                else:
                    logger.warn("Error on attempting to start mission : {}"
                                .format(str(e)))
                    logger.warn("Will attempt again after {} seconds."
                                .format(self.params.retry_sleep))
                    time.sleep(self.params.retry_sleep)

        logger.info("Waiting for mission to start...")
        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                print("Error", error)
                logger.warn(error.text)

        logger.info("Mission Running")
        frame = self._get_video_frame(world_state)
        return frame

    def _get_world_state(self):
        # patiently wait till we get the next observation
        while True:
            time.sleep(self.params.step_sleep)
            world_state = self.agent_host.peekWorldState()
            print("World State : ", world_state)
            if world_state.number_of_observations_since_last_state > \
                    self.skip_steps or not world_state.is_mission_running:
                break
        return self.agent_host.getWorldState()

    def _get_video_frame(self, world_state):
        if world_state.number_of_video_frames_since_last_state > 0:
            assert len(world_state.video_frames) == 1
            frame = world_state.video_frames[0]

            image = np.frombuffer(frame.pixels, dtype=np.uint8)
            image = image.reshape((frame.height, frame.width, frame.channels))
            print("Frame Receieved : ".format(image.shape))
            self.last_image = image
        else:
            # can happen only when mission ends before we get frame
            # then just use the last frame, it doesn't matter much anyway
            image = self.last_image
        return image
