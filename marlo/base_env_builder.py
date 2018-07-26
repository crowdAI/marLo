#!/usr/bin/env python
import gym

from jinja2 import Environment as jinja2Environment
from jinja2 import FileSystemLoader as jinja2FileSystemLoader

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class MarloEnvBuilderBase(gym.Env):
    """
    Base class for all Marlo environment builders
    """
    def __init__(self, templates_folder):
        self.templates_folder = templates_folder
        self.setup_templating()
        self._default_base_params = False

    def setup_templating(self):
        self.jinja2_fileloader = jinja2FileSystemLoader(self.templates_folder)
        self.jinj2_env = jinja2Environment(loader=self.jinja2_fileloader)

    def render_mission_spec(self):
        template = self.jinj2_env.get_template("mission.xml")
        return template.render(
            params=self.params
        )
    
    @property
    def default_base_params(self):
        if not self._default_base_params:
            self._default_base_params = dotdict(
                 role=0,
                 experiment_id="something",
                 continuous_discrete=True, 
                 add_noop_command=None,
                 max_retries=30, 
                 retry_sleep=3, 
                 step_sleep=0.001, 
                 skip_steps=0,
                 videoResolution=None, 
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
