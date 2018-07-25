#!/usr/bin/env python

from jinja2 import Environment as jinja2Environment
from jinja2 import FileSystemLoader as jinja2FileSystemLoader


class MarloEnvBuilderBase:
    """
    Base class for all Marlo environment builders
    """
    def __init__(self, templates_folder):
        self.templates_folder = templates_folder
        self.setup_templating()

    def setup_templating(self):
        self.jinja2_fileloader = jinja2FileSystemLoader(self.templates_folder)
        self.jinj2_env = jinja2Environment(loader=self.jinja2_fileloader)

    def render(self):
        template = self.jinj2_env.get_template("mission.xml")
        return template.render(
            params=self.params
        )
