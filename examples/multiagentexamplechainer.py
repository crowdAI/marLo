import argparse
import gym
import marlo
from gym.envs.registration import register

import time
from marlo.multiagent import start_agents

import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl
import gym
import numpy as np


class QFunction(chainer.Chain):

    def __init__(self, obs_size, n_actions, n_hidden_channels=50):
        super().__init__()
        with self.init_scope():
            self.l0 = L.Linear(obs_size, n_hidden_channels)
            self.l1 = L.Linear(n_hidden_channels, n_hidden_channels)
            self.l2 = L.Linear(n_hidden_channels, n_actions)

    def __call__(self, x, test=False):
        """
        Args:
            x (ndarray or chainer.Variable): An observation
            test (bool): a flag indicating whether it is in test mode
        """
        h = F.tanh(self.l0(x))
        h = F.tanh(self.l1(h))
        return chainerrl.action_value.DiscreteActionValue(self.l2(h))


def main():
    """Running Malmo gym env for multiple agents with chainer."""

    parser = argparse.ArgumentParser(description='Multi-agent example')
    parser.add_argument('--rollouts', type=int, default=1, help='number of rollouts')
    # Example missions: 'pig_chase.xml' or 'bb_mission_1.xml' or 'th_mission_1.xml'
    parser.add_argument('--mission_file', type=str, default="basic.xml", help='the mission xml')
    parser.add_argument('--turn_based', action='store_true')
    args = parser.parse_args()

    number_of_rollouts = args.rollouts
    turn_based = args.turn_based

    # Register the multi-agent environment.
    env_name = 'malmo-multi-agent-v0'

    register(
        id=env_name,
        entry_point='marlo.envs:MinecraftEnv',
        # Make sure mission xml is in the marlo/assets directory.
        kwargs={'mission_file': args.mission_file}
    )

    env = gym.make(env_name)

    resolution = [84, 84]  # [800, 600]
    config = {'allowDiscreteMovement': ["move", "turn"], 'videoResolution': resolution, "turn_based": turn_based}

    join_agents = start_agents(env, env_name, None, config, number_of_rollouts)

    env.init(**config)

    obs_size = 84 * 84 * 3
    n_actions = env.action_space.n
    q_func = QFunction(obs_size, n_actions)

    # Uncomment to use CUDA
    # q_func.to_gpu(0)

    # Use Adam to optimize q_func. eps=1e-2 is for stability.
    optimizer = chainer.optimizers.Adam(eps=1e-2)
    optimizer.setup(q_func)

    # Set the discount factor that discounts future rewards.
    gamma = 0.95

    # Use epsilon-greedy for exploration
    explorer = chainerrl.explorers.ConstantEpsilonGreedy(
        epsilon=0.3, random_action_func=env.action_space.sample)

    # DQN uses Experience Replay.
    # Specify a replay buffer and its capacity.
    replay_buffer = chainerrl.replay_buffer.ReplayBuffer(capacity=10 ** 6)

    # Since observations from CartPole-v0 is numpy.float64 while
    # Chainer only accepts numpy.float32 by default, specify
    # a converter as a feature extractor function phi.
    phi = lambda x: x.astype(np.float32, copy=False)

    # Now create an agent that will interact with the environment.
    agent = chainerrl.agents.DoubleDQN(
        q_func, optimizer, replay_buffer, gamma, explorer,
        replay_start_size=500, update_interval=1,
        target_update_interval=100, phi=phi)

    # Train
    n_episodes = number_of_rollouts
    max_episode_len = 10 ** 6
    for i in range(1, n_episodes + 1):
        print("reset agent 0")
        obs = env.reset()
        reward = 0
        done = False
        R = 0  # return (sum of rewards)
        t = 0  # time step
        print("run 0")
        while not done and t < max_episode_len:
            # Uncomment to watch the behaviour
            # env.render()
            action = agent.act_and_train(obs, reward)
            obs, reward, done, _ = env.step(action)
            R += reward
            t += 1

        if i % 1 == 0:
            print('episode:', i,
                  'R:', R,
                  'statistics:', agent.get_statistics())
        agent.stop_episode_and_train(obs, reward, done)
    print('Finished.')

    join_agents()

    # Evaluate

    print("evaluate")
    number_of_evals = 1

    join_agents = start_agents(env, env_name, None, config, number_of_evals)

    env.init(**config)

    for i in range(number_of_evals):
        obs = env.reset()

        done = False
        R = 0
        t = 0
        while not done and t < max_episode_len:
            env.render()
            action = agent.act(obs)
            obs, r, done, _ = env.step(action)
            R += r
            t += 1
        print('test episode:', i, 'R:', R)
        agent.stop_episode()

    join_agents()

    print("save agent")
    # Save an agent to the 'agent' directory
    agent.save('agent')

    # Uncomment to load an agent from the 'agent' directory
    # agent.load('agent')


if __name__ == "__main__":
    main()
