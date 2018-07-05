import gym
import time
from threading import Thread
from lxml import etree
import uuid


def _run_agent(env_name, config, role, rounds):
    """thread function to run an agent in open ai gym"""

    print("Agent role [" + str(role) + "]")
    env = gym.make(env_name)
    config2 = config.copy()
    config2['role'] = role
    config2['videoResolution'] = [84, 84]
    print(config2)
    env.init(**config2)

    for i in range(rounds):
        print("reset " + str(role) + " for new game " + str(i + 1))
        env.reset()

        done = False
        while not done:

            # Background agents are random for training. Not to be relied upon :-)
            action = env.action_space.sample()

            obs, reward, done, info = env.step(action)

    env.close()


def start_agents(env, env_name, config, number_of_rollouts, daemon=False):
    """Start background agents in multi-agent games"""

    xml = etree.parse(env.mission_file)
    number_of_agents = len(xml.getroot().findall('{http://ProjectMalmo.microsoft.com}AgentSection'))

    # Create and run one thread for each agent section in the xml.
    experiment_id = str(uuid.uuid4())
    client_pool = [('127.0.0.1', 10000 + i) for i in range(number_of_agents)]
    config['role'] = 0
    config['client_pool'] = client_pool
    config['experiment_id'] = experiment_id

    threads = [Thread(target=_run_agent, args=(env_name, config, t + 1, number_of_rollouts), daemon=daemon)
               for t in range(number_of_agents - 1)]
    [t.start() for t in threads]
    return lambda: [t.join() for t in threads]
