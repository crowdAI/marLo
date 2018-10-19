import marlo
import time
import json
import base64
import random
import argparse
import itertools

parser = argparse.ArgumentParser(description='random test marlo comp xml')
parser.add_argument('--episodes', type=int, default=10, help='number of episodes')
args = parser.parse_args()

games = ("BuildbattleTrain", "MobchaseTrain", "TreasurehuntTrain")
missions = [x for x in itertools.chain.from_iterable([[games[0] + str(i),
                                                       games[1] + str(i),
                                                       games[2] + str(i)] for i in range(1, 6)])]
print(missions)

client_pool = [('127.0.0.1', 10000), ('127.0.0.1', 10001)]
all_join_tokens = [marlo.make('MarLo-' + mission + '-v0',
                              params={
                                  "client_pool": client_pool,
                                  "agent_names":
                                      [
                                          "MarLo-Agent-0",
                                          "MarLo-Agent-1"
                                      ],
                                  "comp_all_commands": ["move", "turn", "use"]
                              }) for mission in missions]


@marlo.threaded
def run_agent(token, agent_role):
    env = marlo.init(token)
    env.reset()
    done = False
    while not done:
        if agent_role == 0:
            # TODO YOUR AGENT HERE
            _action = env.action_space.sample()
        else:
            # TODO OTHER AGENT HERE
            _action = env.action_space.sample()
        obs, reward, done, info = env.step(_action)
        time.sleep(0.05)
        print("Agent " + str(agent_role) + " reward:", reward)
        # print("Agent " + str(agent_role) + " obs:", str(obs))
        # print("Agent " + str(agent_role) + " done:", done)
        # print("Agent " + str(agent_role) + " info", info)
    env.close()


episodes = 0
while episodes < args.episodes:
    episodes += 1
    print("run " + str(episodes))
    join_tokens = random.choice(all_join_tokens)
    threads = [run_agent(join_token, i)[0] for i, join_token in enumerate(join_tokens)]
    [t.join() for t in threads]


