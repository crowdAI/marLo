
## Configuration options

These are parameters to env.init() method. While it is possible to call env.init() several times, giving only one parameter each time, it is safer to include all parameters in one call.
Technical

* `client_pool` = None - list of Minecraft instances to connect to. The arguments should be list of tuples in form [('127.0.0.1', 10000), ('127.0.0.1', 10001)]. The agent tries all addresses in sequence and uses first free instance. Default is empty, which means [('127.0.0.1', 10000)].

* `max_retries` = 90 - how many times to retry initialization of mission (in `env.reset()`) before giving up. Default is 90.
* `retry_sleep` = 10 - how many seconds to sleep before trying mission initialization again during reset. Default is 10.
* `step_sleep` = 0.001 - how long to sleep between making action and waiting for observation. Default value 0.001 means that new observation is checked max 1000 times in second. That seemed acceptable with 5ms ticks (200 ticks per second). Using `step_sleep = 0` might reduce number of lost observations a tiny amount, but at the cost of substantially higher CPU usage. NB! gym-minecraft always waits for at least one Minecraft tick to occur and ignores video frames sent in meantime.
* `skip_steps` = 0 - how many observations to skip. For example to process every 4th observation set `skip_steps = 3`.
* `continuous_discrete` = False - convert continuous action space to discrete, i.e. when allowed continuous actions are 'move' and 'turn', then discrete action space contains 4 actions: move -1, move 1, turn -1, turn 1.
* `add_noop_command` = None - add also no-operation discrete action, that is currently fixed to move 0\nturn 0.

## Observations

* `videoResolution` = None - resolution for video frames as tuple (width, height). Default is to use video resolution from XML,
* `videoWithDepth` = None - if True, then use video with depth component, observations are going to have 4 channels. Default is to use settings from XML.
* `observeRecentCommands` = None - if True, then recent commands are included in info part of observation.
* `observeHotBar` = None - if True, then hotbar state is included in info part of observation.
* `observeFullInventory` = None - if True, then inventory state is included in info part of observation.
* `observeGrid` = None - include agent surroundings as grid in info part of observation. The value should be tuple of (x1, y1, z1, x2, y2, z2), where the curresponding elements are shifts from agent's current location. The corresponding element in info is named "grid".
* `observeDistance` = None - include distance to particular point in info part of observation. The value should be (x, y, z), i.e. the coordinates of destination. The corresponding element in info is named "dist".
* `observeChat` = None - if True, then chat messages are included in info part of observation.

## Actions

* `allowContinuousMovement` = None - if True, then allow all continuous movement commands. If list, then allow particular commands listed in this list.
* `allowDiscreteMovement` = None - if True, then allow all discrete movement commands. If list, then allow particular commands listed in this list.
* `allowAbsoluteMovement` = None - if True, then allow all absolute movement commands. If list, then allow particular commands listed in this list. Not supported yet.

By default all actions from XML file are allowed. If any of the above configuration options is used, then XML settings are discarded and only chosen commands are allowed.
Recording

These mirror MissionRecordSpec methods, see [their documentation](http://microsoft.github.io/malmo/0.17.0/Documentation/structmalmo_1_1_mission_record_spec.html).

* `recordDestination` = None
* `recordObservations` = None
* `recordRewards` = None
* `recordCommands` = None
* `recordMP4` = None

## Other

* `gameMode` = None - either survival (default), spectator or creative. Haven't found much use for these yet.
* `forceWorldReset` = None - if True, then create a new random world at each env.reset(). Only meaningful for some worlds, i.e. `MinecraftDefaultFlat1-v0`, `MinecraftTrickyArena1-v0`, etc.

## Additional methods

In addition to `init()` there are two methods to sneak in custom Malmo missions:

    * `env.load_mission_file(file_path)` - load custom mission file instead of one of the predetermined worlds.
    * `env.load_mission_xml(xml)` - the same as previous, only XML string should be passed.
