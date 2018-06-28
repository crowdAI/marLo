import argparse
import gym
import marlo
from gym.envs.registration import register

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
        print("reset for new game " + str(i + 1))
        env.reset()

        done = False
        while not done:

            # Background agents are random for training. Not to be relied upon :-)
            action = env.action_space.sample()

            obs, reward, done, info = env.step(action)
            print(action)

    env.close()


def start_agents(env, env_name, config, number_of_rollouts):
    """Start background agents in multi-agent games"""

    xml = etree.parse(env.mission_file)
    number_of_agents = len(xml.getroot().findall('{http://ProjectMalmo.microsoft.com}AgentSection'))

    # Create and run one thread for each agent section in the xml.
    experiment_id = str(uuid.uuid4())
    client_pool = [('127.0.0.1', 10000 + i) for i in range(number_of_agents)]
    config['role'] = 0
    config['client_pool'] = client_pool
    config['experiment_id'] = experiment_id

    threads = [Thread(target=_run_agent, args=(env_name, config, t + 1, number_of_rollouts))
               for t in range(number_of_agents - 1)]
    [t.start() for t in threads]
    return lambda: [t.join() for t in threads]


def main():
    """Running Malmo gym env with multiple agents."""

    parser = argparse.ArgumentParser(description='Multi-agent example')
    parser.add_argument('--rollouts', type=int, default=1, help='number of rollouts')
    # Example missions: 'pig_chase.xml' or 'bb_mission_1.xml' or 'th_mission_1.xml'
    parser.add_argument('--mission_file', type=str, default="basic.xml", help='the mission xml')
    args = parser.parse_args()

    number_of_rollouts = args.rollouts

    # Register the multi-agent environment.
    env_name = 'malmo-multi-agent-v0'

    register(
        id=env_name,
        entry_point='marlo.envs:MinecraftEnv',
        # Make sure mission xml is in the marlo/assets directory.
        kwargs={'mission_file': args.mission_file}
    )

    # Create one env to obtain the mission xml.
    env = gym.make(env_name)

    resolution = [84, 84]  # [800, 600]
    config = {'allowContinuousMovement': ["move", "turn"], 'videoResolution': resolution}

    join_agents = start_agents(env, env_name, config, number_of_rollouts)

    env.init(**config)

    for i in range(number_of_rollouts):
        print("reset for new game " + str(i + 1))
        env.reset()

        done = False
        while not done:
            env.render("rgb_array")

            # TODO your agent here.
            action = env.action_space.sample()

            obs, reward, done, info = env.step(action)
            print(reward)
            print(obs)

    env.close()
    join_agents()


if __name__ == "__main__":
    main()
