import marlo
import time
import json
import base64
import random
import argparse
import itertools

print("testing 123")

parser = argparse.ArgumentParser(description='random test marlo comp xml')
parser.add_argument('--episodes', type=int, default=10, help='number of episodes')
args = parser.parse_args()

missionnames = ("BuildbattleTrain", "MobchaseTrain", "TreasurehuntTrain")
missions = [x for x in itertools.chain.from_iterable([[missionnames[0] + str(i), missionnames[1] + str(i), missionnames[2] + str(i)] for i in range(1, 6)])]

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
def run_agent(join_token):
    env = marlo.init(join_token)
    frame = env.reset()
    done = False
    count = 0
    while not done:
        _action = env.action_space.sample()
        obs, reward, done, info = env.step(_action)
        time.sleep(0.05)
        # print("reward:", reward)
        # print("done:", done)
        # print("info", info)
    env.close()


episodes = 0

while episodes < args.episodes:
    episodes += 1
    join_tokens = random.choice(all_join_tokens)
    threads = [run_agent(join_token)[0] for join_token in join_tokens]
    [t.join() for t in threads]



