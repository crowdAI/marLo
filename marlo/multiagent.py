import gym
import time
from threading import Thread
from lxml import etree
import uuid


class RandomBackgroundAgent(object):

    def __init__(self, env):
        self._env = env

    def create_agent(self, env):
        return RandomBackgroundAgent(env)

    def action(self, obs):
        return self._env.action_space.sample()


def _run_agent(env_name, background_agent, config, role, rounds):
    """thread function to run an agent in open ai gym"""

    print("Agent role [" + str(role) + "]")
    env = gym.make(env_name)
    config2 = config.copy()
    config2['role'] = role
    config2['videoResolution'] = [84, 84]
    print(config2)
    env.init(**config2)

    agent = background_agent.create_agent(env)

    for i in range(rounds):
        print("reset agent " + str(role) + " for new game " + str(i + 1))
        env.reset()

        obs = None
        done = False
        while not done:
            action = agent.action(obs)
            obs, reward, done, info = env.step(action)

    env.close()


def start_agents(env, env_name, background_agent, config, number_of_rollouts, daemon=False):
    """Start background agents in multi-agent games"""

    if background_agent is None:
        background_agent = RandomBackgroundAgent(env)

    xml = etree.parse(env.mission_file)
    number_of_agents = len(xml.getroot().findall('{http://ProjectMalmo.microsoft.com}AgentSection'))

    # Create and run one thread for each agent section in the xml.
    experiment_id = str(uuid.uuid4())
    client_pool = [('127.0.0.1', 10000 + i) for i in range(number_of_agents)]
    config['role'] = 0
    config['client_pool'] = client_pool
    config['experiment_id'] = experiment_id

    threads = [Thread(target=_run_agent, args=(env_name, background_agent, config, t + 1, number_of_rollouts), daemon=daemon)
               for t in range(number_of_agents - 1)]
    [t.start() for t in threads]
    return lambda: [t.join() for t in threads]
