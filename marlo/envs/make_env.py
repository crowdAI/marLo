
import argparse
import os
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(description='Make a Marlo Env')

parser.add_argument('--name', type=str, required=True, help='the environment name')
parser.add_argument('--mission_file', type=str, required=True, help='the mission file')
parser.add_argument('--description', type=str, default=None, help='a brief description of the env')
args = parser.parse_args()

print("Make env " + args.name)

env_dir = args.name
if not os.path.exists(env_dir):
    os.makedirs(env_dir)

templates_dir = env_dir + "/templates"
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

mission_file = Path(args.mission_file)
if not mission_file.exists():
    print("Mission file does not exist!")
    exit(-1)

shutil.copy(args.mission_file, templates_dir + "\\mission.xml")

if args.description is None:
    description = ""
else:
    desciption_file = Path(args.description)
    if not desciption_file.exists():
        print("description file does not exist")
        exit(-2)
    description = desciption_file.read_text()

init_py = """
import gym
from .main import MarloEnvBuilder


def _register():
    ##########################################
    # Version 0 of env
    ##########################################
    gym.envs.registration.register(
        id='MarLo-%ENV_NAME%-v0',
        entry_point=MarloEnvBuilder
    )
""".replace("%ENV_NAME%", args.name)

init_file = env_dir + "/__init__.py"
Path(init_file).write_text(init_py)

main_py = """import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython
import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    %ENV_DESCRIPTION%
    
    def __init__(self, extra_params=None):
        if extra_params is None:
            extra_params={}
        super(MarloEnvBuilder, self).__init__(
                templates_folder=os.path.join(
                            str(Path(__file__).parent),
                            "templates"
                )
        )
        self.params = self._default_params()
        # You can do something with the extra_params if you wish

    def _default_params(self):
        _default_params = super(MarloEnvBuilder, self).default_base_params
        return _default_params


if __name__ == "__main__":
    env_builder = MarloEnvBuilder()
    mission_xml = env_builder.render_mission_spec()
    mission_spec = MalmoPython.MissionSpec(mission_xml, True)
    print(mission_spec.getSummary())

""".replace('%ENV_DESCRIPTION%', '"""\n' + description + '"""')

main_file = env_dir + "/main.py"
Path(main_file).write_text(main_py)
