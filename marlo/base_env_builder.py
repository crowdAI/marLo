#!/usr/bin/env python
import time
import json
import gym
import numpy as np
import marlo
from marlo import MalmoPython
import uuid
import hashlib
import base64

import xml.etree.ElementTree as ElementTree

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


class TurnState(object):
    def __init__(self):
        self._turn_key = None
        self._has_played = False

    def update(self, key):
        self._has_played = False
        self._turn_key = key

    @property
    def can_play(self):
        return self._turn_key is not None and not self._has_played

    @property
    def key(self):
        return self._turn_key

    @property
    def has_played(self):
        return self._has_played

    @has_played.setter
    def has_played(self, value):
        self._has_played = bool(value)


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
        self.experiment_id = None
        
        self._turn = None

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
            "client_pool",
            "allowContinuousMovement",
            "continuous_to_discrete"
            "recordMP4"
        ]

    @property
    def default_base_params(self):
        if not self._default_base_params:
            self._default_base_params = dotdict(
                 seed="random",
                 tick_length=50,
                 role=0,
                 experiment_id="something",
                 client_pool = None,
                 add_noop_command=True,
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
                 continuous_to_discrete=True,
                 allowContinuousMovement=True,
                 allowDiscreteMovement=True,
                 allowAbsoluteMovement=False,
                 recordDestination=None,
                 recordObservations=None,
                 recordRewards=None,
                 recordCommands=None,
                 recordMP4=None,
                 gameMode=None,
                 forceWorldReset=True,
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
                        if params.continuous_to_discrete:
                            discrete_actions.append(command + " 1")
                            discrete_actions.append(command + " -1")
                        else:
                            continuous_actions.append(command)
                    elif command in ["crouch", "jump", "attack", "use"]:
                        if params.continuous_to_discrete:
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
                    logger.warn(
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
        if not params.client_pool:
            logger.warn("No client pool provided, attempting to create "
                         "a client_pool of the correct size")
            number_of_agents = self.mission_spec.getNumberOfAgents()
            params.client_pool = marlo.launch_clients(number_of_agents)
            
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
                assert type(params.recordMP4) == list \
                    and len(params.recordMP4) == 2
                self.mission_record_spec.recordMP4(*(params.recordMP4))
        else:
            if params.recordRewards or params.recordCommands  or params.recordMP4:
                raise Exception("recordRewards or recordCommands or recordMP4 "
                                "provided without specifyin recordDestination")

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

    def setup_mission_spec(self, params):
        ############################################################
        # Instantiate Mission Spec
        ############################################################
        mission_xml = self.render_mission_spec()
        self.mission_spec = MalmoPython.MissionSpec(mission_xml, True)

    def setup_turn_based_games(self, params):
        if params.turn_based:
            self._turn = TurnState()

    def init(self, params, dry_run=False):
        self.params.update(params)
        self.dry_run = dry_run
        self.build_env(self.params)
        number_of_agents = self.mission_spec.getNumberOfAgents()
        mission_xml = self.mission_spec.getAsXML(False)
        join_tokens = []
        experiment_id = str(uuid.uuid4())
        for _idx in range(number_of_agents):
            _join_token = {}
            _join_token["role"] = _idx
            _join_token["mission_xml"] = mission_xml
            _join_token["experiment_id"] = experiment_id
            _join_token["game_params"] = self.params
            _join_token = base64.b64encode(
                    json.dumps(_join_token).encode('utf8')
            )
            join_tokens.append(_join_token)
        return join_tokens

    def build_env(self, params):
        self.setup_mission_spec(params)
        self.setup_turn_based_games(params)

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
    def reset(self):
        if self.params.forceWorldReset:
            # Force a World Reset on each reset
            self.mission_spec.forceWorldReset()

        # Attempt to start a mission
        for retry in range(self.params.max_retries + 1):
            logger.debug("RETRY : {}".format(retry))
            # Role 0 (the server) could take some extra time to start
            if self.params.role != 0:
                time.sleep(1)
            else:
                time.sleep(0.1)

            if self.params.experiment_id:
                self.experiment_id = self.params.experiment_id

            try:
                if not self.client_pool:
                    raise Exception("client_pool not specified.")
                self.agent_host.startMission(
                    self.mission_spec,
                    self.client_pool,
                    self.mission_record_spec,
                    self.params.role,
                    self.experiment_id
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
                logger.error("Error", error)
                logger.warn(error.text)

        logger.info("Mission Running")
        frame = self._get_video_frame(world_state)
        return frame

    def _get_world_state(self):
        # patiently wait till we get the next observation
        while True:
            time.sleep(self.params.step_sleep)
            world_state = self.agent_host.peekWorldState()
            if world_state.number_of_observations_since_last_state > \
                    self.params.skip_steps or not world_state.is_mission_running:
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

    def _get_observation(self, world_state):
        if world_state.number_of_observations_since_last_state > 0:
            missed = world_state.number_of_observations_since_last_state \
                    - len(world_state.observations) - self.params.skip_steps
            if missed > 0:
                logger.warn("Agent missed %d observation(s).", missed)
            assert len(world_state.observations) == 1
            return json.loads(world_state.observations[0].text)
        else:
            return None

    def _send_command(self, command):
        if self._turn:
            self.agent_host.sendCommand(command, self._turn.key)
            self._turn.has_payed = True
        else:
            logger.debug("Send Command : {}".format(command))
            self.agent_host.sendCommand(command)

    def _take_action(self, actions):
        # no tuple in case of a single action
        if len(self.action_spaces) == 1:
            actions = [actions]

        if self._turn:
            if not self._turn.can_play:
                return

        # send corresponding command
        for _spaces, _commands, _actions in \
                zip(self.action_spaces, self.action_names, actions):

            if isinstance(_spaces, gym.spaces.Discrete):
                logger.debug(_commands[_actions])
                # print("cmd " + cmds[acts])
                self._send_command(_commands[_actions])
            elif isinstance(_spaces, gym.spaces.Box):
                for command, value in zip(_commands, _actions):
                    _command = "{}-{}".format(command, value)
                    logger.debug(_command)
                    self._send_command(_command)
            elif isinstance(_spaces, gym.spaces.MultiDiscrete):
                for command, value in zip(_commands, _actions):
                    _command = "{}-{}".format(command, value)
                    logger.debug(_command)
                    self._send_command(_command)
            else:
                logger.warn("Ignoring unknown action space for {}".format(
                    _commands
                    ))

    def step(self, action):
        world_state = self.agent_host.peekWorldState()
        if world_state.is_mission_running:
            self._take_action(action)

        world_state = self._get_world_state()

        # Update turn state
        if world_state.number_of_observations_since_last_state > 0:
            data = json.loads(world_state.observations[-1].text)
            turn_key = data.get(u'turn_key', None)
            if turn_key is not None and turn_key != self._turn.key:
                self._turn.update(turn_key)

        # Log
        for error in world_state.errors:
            logger.warn(error.text)
        for message in world_state.mission_control_messages:
            logger.debug(message.text)
            root = ElementTree.fromstring(message.text)
            if root.tag == '{http://ProjectMalmo.microsoft.com}MissionEnded':
                for el in root.findall(
                        '{http://ProjectMalmo.microsoft.com}HumanReadableStatus' # noqa: E501
                        ):
                    logger.info("Mission ended: %s", el.text)

        # Compute Rewards
        reward = 0
        for _reward in world_state.rewards:
            print(_reward)
            reward += _reward.getValue()

        # Get observation
        image = self._get_video_frame(world_state)

        # detect if done ?
        done = not world_state.is_mission_running

        # gather info
        info = {}
        info['has_mission_begun'] = world_state.has_mission_begun
        info['is_mission_running'] = world_state.is_mission_running
        info['number_of_video_frames_since_last_state'] = world_state.number_of_video_frames_since_last_state # noqa: E501
        info['number_of_rewards_since_last_state'] = world_state.number_of_rewards_since_last_state # noqa: E501
        info['number_of_observations_since_last_state'] = world_state.number_of_observations_since_last_state # noqa: E501
        info['mission_control_messages'] = [msg.text for msg in world_state.mission_control_messages] # noqa: E501
        info['observation'] = self._get_observation(world_state)

        return image, reward, done, info

    def render(self, mode='rgb_array', close=False):
        if mode == "rgb_array":
            return self.last_image
        elif mode == "human":
            # TODO: Implement this
            raise None
        else:
            raise NotImplemented("Render Mode not implemented : {}"
                                 .format(mode))

    def seed(self, seed=None):
        self.mission_spec.setWorldSeed(str(seed))
        return [seed]
