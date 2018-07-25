import logging
import time
import os
from pathlib import Path
import numpy as np
import json
import xml.etree.ElementTree as ET
import gym
from gym import spaces, error

reshape = False

try:
    import malmo.MalmoPython as MalmoPython
except ImportError as e:
    err = e
    try:
        import MalmoPython
    except ImportError:
        raise error.DependencyNotInstalled("{}. Malmo doesn't seem to be installed."
                "Please install Malmo from GitHub or with \"pip3 install malmo\".".format(err))

logger = logging.getLogger(__name__)

SINGLE_DIRECTION_DISCRETE_MOVEMENTS = [ "jumpeast", "jumpnorth", "jumpsouth", "jumpwest",
                                        "movenorth", "moveeast", "movesouth", "movewest",
                                        "jumpuse", "use", "attack", "jump" ]

MULTIPLE_DIRECTION_DISCRETE_MOVEMENTS = [ "move", "turn", "look", "strafe",
                                          "jumpmove", "jumpstrafe" ]


class InvalidMissionFile(Exception):
    def __init__(self, file_name):
        self.file_name = file_name


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


class MinecraftEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, mission_file):
        super(MinecraftEnv, self).__init__()

        self.agent_host = MalmoPython.AgentHost()

        # Allow full paths for mission files.
        if Path(mission_file).is_file():
            self.mission_file = mission_file
        else:
            assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets')
            self.mission_file = os.path.join(assets_dir, mission_file)
            if not Path(self.mission_file).is_file():
                raise InvalidMissionFile(mission_file)

        self.load_mission_file(self.mission_file)

        self.client_pool = None
        self.mc_process = None
        self.screen = None
        self.experiment_id = None
        self._turn = None

    def load_mission_file(self, mission_file):
        logger.info("Loading mission from " + mission_file)
        mission_xml = open(mission_file, 'r').read()
        self.load_mission_xml(mission_xml)

    def load_mission_xml(self, mission_xml):
        self.mission_spec = MalmoPython.MissionSpec(mission_xml, True)
        logger.info("Loaded mission: " + self.mission_spec.getSummary())

    def init(self, client_pool=None, role=0,
             continuous_discrete=True, add_noop_command=None,
             max_retries=30, retry_sleep=3, step_sleep=0.001, skip_steps=0,
             videoResolution=None, videoWithDepth=None,
             observeRecentCommands=None, observeHotBar=None,
             observeFullInventory=None, observeGrid=None,
             observeDistance=None, observeChat=None,
             allowContinuousMovement=None, allowDiscreteMovement=None,
             allowAbsoluteMovement=None, recordDestination=None,
             recordObservations=None, recordRewards=None,
             recordCommands=None, recordMP4=None,
             gameMode=None, forceWorldReset=None,
             turn_based=False,
             experiment_id="experimentid"):

        self.role = role
        self.max_retries = max_retries
        self.retry_sleep = retry_sleep
        self.step_sleep = step_sleep
        self.skip_steps = skip_steps
        self.forceWorldReset = forceWorldReset
        self.continuous_discrete = continuous_discrete
        self.add_noop_command = add_noop_command
        self.experiment_id = experiment_id
        if turn_based:
            self._turn = TurnState()

        if videoResolution:
            if videoWithDepth:
                self.mission_spec.requestVideoWithDepth(*videoResolution)
            else:
                self.mission_spec.requestVideo(*videoResolution)

        if observeRecentCommands:
            self.mission_spec.observeRecentCommands()
        if observeHotBar:
            self.mission_spec.observeHotBar()
        if observeFullInventory:
            self.mission_spec.observeFullInventory()
        if observeGrid:
            self.mission_spec.observeGrid(*(observeGrid + ["grid"]))
        if observeDistance:
            self.mission_spec.observeDistance(*(observeDistance + ["dist"]))
        if observeChat:
            self.mission_spec.observeChat()

        if allowContinuousMovement or allowDiscreteMovement or allowAbsoluteMovement:
            # if there are any parameters, remove current command handlers first
            self.mission_spec.removeAllCommandHandlers()

            if allowContinuousMovement is True:
                self.mission_spec.allowAllContinuousMovementCommands()
            elif isinstance(allowContinuousMovement, list):
                for cmd in allowContinuousMovement:
                    self.mission_spec.allowContinuousMovementCommand(cmd)

            if allowDiscreteMovement is True:
                self.mission_spec.allowAllDiscreteMovementCommands()
            elif isinstance(allowDiscreteMovement, list):
                for cmd in allowDiscreteMovement:
                    self.mission_spec.allowDiscreteMovementCommand(cmd)

            if allowAbsoluteMovement is True:
                self.mission_spec.allowAllAbsoluteMovementCommands()
            elif isinstance(allowAbsoluteMovement, list):
                for cmd in allowAbsoluteMovement:
                    self.mission_spec.allowAbsoluteMovementCommand(cmd)

        if client_pool:
            if not isinstance(client_pool, list):
                raise ValueError("client_pool must be list of tuples of (IP-address, port)")
            self.client_pool = MalmoPython.ClientPool()
            for client in client_pool:
                self.client_pool.add(MalmoPython.ClientInfo(*client))

        # TODO: produce observation space dynamically based on requested features

        self.video_height = self.mission_spec.getVideoHeight(0)
        self.video_width = self.mission_spec.getVideoWidth(0)
        self.video_depth = self.mission_spec.getVideoChannels(0)
        self.observation_space = spaces.Box(
                low=0, high=255,
                shape=(self.video_height, self.video_width, self.video_depth),
                dtype=np.uint8
                )
        # dummy image just for the first observation
        # self.last_image = np.zeros((self.video_height, self.video_width, self.video_depth), dtype=np.uint8)
        self.last_image = np.zeros((self.video_height * self.video_width * self.video_depth), dtype=np.uint8)
        self._create_action_space()

        # mission recording
        self.mission_record_spec = MalmoPython.MissionRecordSpec()  # record nothing
        if recordDestination:
            self.mission_record_spec.setDestination(recordDestination)
        if recordRewards:
            self.mission_record_spec.recordRewards()
        if recordCommands:
            self.mission_record_spec.recordCommands()
        if recordMP4:
            self.mission_record_spec.recordMP4(*recordMP4)

        if gameMode:
            if gameMode == "spectator":
                self.mission_spec.setModeToSpectator()
            elif gameMode == "creative":
                self.mission_spec.setModeToCreative()
            elif gameMode == "survival":
                logger.warn("Cannot force survival mode, assuming it is the default.")
            else:
                assert False, "Unknown game mode: " + gameMode

    def _create_action_space(self):
        # collect different actions based on allowed commands
        continuous_actions = []
        discrete_actions = []
        multidiscrete_actions = []
        multidiscrete_action_ranges = []
        if self.add_noop_command:
            # add NOOP command
            discrete_actions.append("move 0\nturn 0")
        chs = self.mission_spec.getListOfCommandHandlers(0)
        for ch in chs:
            cmds = self.mission_spec.getAllowedCommands(0, ch)
            for cmd in cmds:
                logger.debug(ch + ":" + cmd)
                if ch == "ContinuousMovement":
                    if cmd in ["move", "strafe", "pitch", "turn"]:
                        if self.continuous_discrete:
                            discrete_actions.append(cmd + " 1")
                            discrete_actions.append(cmd + " -1")
                        else:
                            continuous_actions.append(cmd)
                    elif cmd in ["crouch", "jump", "attack", "use"]:
                        if self.continuous_discrete:
                            discrete_actions.append(cmd + " 1")
                            discrete_actions.append(cmd + " 0")
                        else:
                            multidiscrete_actions.append(cmd)
                            multidiscrete_action_ranges.append([0, 1])
                    else:
                        raise ValueError("Unknown continuous action " + cmd)
                elif ch == "DiscreteMovement":
                    if cmd in SINGLE_DIRECTION_DISCRETE_MOVEMENTS:
                        discrete_actions.append(cmd + " 1")
                    elif cmd in MULTIPLE_DIRECTION_DISCRETE_MOVEMENTS:
                        discrete_actions.append(cmd + " 1")
                        discrete_actions.append(cmd + " -1")
                    else:
                        raise ValueError(False, "Unknown discrete action " + cmd)
                elif ch == "AbsoluteMovement":
                    # TODO: support for AbsoluteMovement
                    logger.warn("Absolute movement not supported, ignoring.")
                elif ch == "Inventory":
                    # TODO: support for Inventory
                    logger.warn("Inventory management not supported, ignoring.")
                else:
                    logger.warn("Unknown commandhandler " + ch)

        # turn action lists into action spaces
        self.action_names = []
        self.action_spaces = []
        if len(discrete_actions) > 0:
            self.action_spaces.append(spaces.Discrete(len(discrete_actions)))
            self.action_names.append(discrete_actions)
        if len(continuous_actions) > 0:
            self.action_spaces.append(spaces.Box(-1, 1, (len(continuous_actions),)))
            self.action_names.append(continuous_actions)
        if len(multidiscrete_actions) > 0:
            self.action_spaces.append(spaces.MultiDiscrete(multidiscrete_action_ranges))
            self.action_names.append(multidiscrete_actions)

        # if there is only one action space, don't wrap it in Tuple
        if len(self.action_spaces) == 1:
            self.action_space = self.action_spaces[0]
        else:
            self.action_space = spaces.Tuple(self.action_spaces)
        logger.debug(self.action_space)

    def reset(self):

        logger.info("reset agent " + str(self.role))
        # force new world each time
        if self.forceWorldReset:
            self.mission_spec.forceWorldReset()

        # Attempt to start a mission
        for retry in range(self.max_retries + 1):
            # Give the server time to start
            if self.role != 0:
                time.sleep(1)
            else:
                time.sleep(0.1)
            try:
                if self.client_pool:
                    self.agent_host.startMission(self.mission_spec, self.client_pool, self.mission_record_spec,
                                                 self.role, self.experiment_id)
                else:
                    self.agent_host.startMission(self.mission_spec, self.mission_record_spec)
                break
            except RuntimeError as e:
                if retry == self.max_retries:
                    logger.error("Error starting mission: "+str(e))
                    raise
                else:
                    logger.warn("On starting mission: "+str(e))
                    logger.warn("Will retry after %d seconds...", self.retry_sleep)
                    time.sleep(self.retry_sleep)

        # Loop until mission starts:
        logger.info("Waiting for the mission to start")
        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                logger.warn(error.text)

        logger.info("Mission running")

        return self._get_video_frame(world_state)

    def _send_command(self, cmd):
        if self._turn:
            self.agent_host.sendCommand(cmd, self._turn.key)
            self._turn.has_payed = True
        else:
            self.agent_host.sendCommand(cmd)

    def _take_action(self, actions):
        # if there is only one action space, it wasn't wrapped in Tuple
        if len(self.action_spaces) == 1:
            actions = [actions]
        if self._turn:
            if not self._turn.can_play:
                return

        # send appropriate command for different actions
        for spc, cmds, acts in zip(self.action_spaces, self.action_names, actions):
            if isinstance(spc, spaces.Discrete):
                logger.debug(cmds[acts])
                # print("cmd " + cmds[acts])
                self._send_command(cmds[acts])
            elif isinstance(spc, spaces.Box):
                for cmd, val in zip(cmds, acts):
                    # print("cmd " + cmd + " " + str(val))
                    logger.debug(cmd + " " + str(val))
                    self._send_command(cmd + " " + str(val))
            elif isinstance(spc, spaces.MultiDiscrete):
                for cmd, val in zip(cmds, acts):
                    # print("cmd " + cmd + " " + str(val))
                    logger.debug(cmd + " " + str(val))
                    self._send_command(cmd + " " + str(val))
            else:
                logger.warn("Unknown action space for %s, ignoring." % cmds)

    def _get_world_state(self):
        # wait till we have got at least one observation or mission has ended
        while True:
            time.sleep(self.step_sleep)  # wait for 1ms to not consume entire CPU
            world_state = self.agent_host.peekWorldState()
            if world_state.number_of_observations_since_last_state > self.skip_steps or not world_state.is_mission_running:
                break

        return self.agent_host.getWorldState()

    def _get_video_frame(self, world_state):
        # process the video frame
        if world_state.number_of_video_frames_since_last_state > 0:
            assert len(world_state.video_frames) == 1
            frame = world_state.video_frames[0]

            image = np.frombuffer(frame.pixels, dtype=np.uint8)
            if reshape:
                image = image.reshape((frame.height, frame.width, frame.channels))
            logger.debug(image)
            self.last_image = image
        else:
            # can happen only when mission ends before we get frame
            # then just use the last frame, it doesn't matter much anyway
            image = self.last_image

        return image

    def _get_observation(self, world_state):
        if world_state.number_of_observations_since_last_state > 0:
            missed = world_state.number_of_observations_since_last_state - len(world_state.observations) - self.skip_steps
            if False and missed > 0:
                logger.warn("Agent missed %d observation(s).", missed)
            assert len(world_state.observations) == 1
            return json.loads(world_state.observations[0].text)
        else:
            return None

    def step(self, action):
        # take the action only if mission is still running
        world_state = self.agent_host.peekWorldState()
        if world_state.is_mission_running:
            # take action
            self._take_action(action)
        # wait for the new state
        world_state = self._get_world_state()

        # Update turn state
        if world_state.number_of_observations_since_last_state > 0:
            data = json.loads(world_state.observations[-1].text)
            turn_key = data.get(u'turn_key', None)

            if turn_key is not None and turn_key != self._turn.key:
                self._turn.update(turn_key)

        # log errors and control messages
        for error in world_state.errors:
            logger.warn(error.text)
        for msg in world_state.mission_control_messages:
            logger.debug(msg.text)
            root = ET.fromstring(msg.text)
            if root.tag == '{http://ProjectMalmo.microsoft.com}MissionEnded':
                for el in root.findall('{http://ProjectMalmo.microsoft.com}HumanReadableStatus'):
                    logger.info("Mission ended: %s", el.text)

        # sum rewards
        # Get Cumulative Reward 
        reward = 0
        for r in world_state.rewards:
            reward += r.getValue()

        # take the last frame from world state
        image = self._get_video_frame(world_state)

        # detect terminal state
        done = not world_state.is_mission_running

        # other auxiliary data
        info = {}
        info['has_mission_begun'] = world_state.has_mission_begun
        info['is_mission_running'] = world_state.is_mission_running
        info['number_of_video_frames_since_last_state'] = world_state.number_of_video_frames_since_last_state
        info['number_of_rewards_since_last_state'] = world_state.number_of_rewards_since_last_state
        info['number_of_observations_since_last_state'] = world_state.number_of_observations_since_last_state
        info['mission_control_messages'] = [msg.text for msg in world_state.mission_control_messages]
        info['observation'] = self._get_observation(world_state)

        return image, reward, done, info

    def render(self, mode='rgb_array', close=False):
        if mode == 'rgb_array':
            return self.last_image
        elif mode == 'human':
            return None
        else:
            raise error.UnsupportedMode("Unsupported render mode: " + mode)

    def close(self):
        if hasattr(self, 'mc_process') and self.mc_process:
            # To be handled
            foo = 1

    def seed(self, seed=None):
        self.mission_spec.setWorldSeed(str(seed))
        return [seed]
