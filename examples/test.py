import marlo
import time
import json
import base64

import argparse

print("testing 123")

parser = argparse.ArgumentParser(description='test marlo comp xml')
parser.add_argument('--mission', type=str, required=True, help='the mission')
args = parser.parse_args()


client_pool = [('127.0.0.1', 10000),('127.0.0.1', 10001)]
join_tokens = marlo.make('MarLo-' + args.mission + '-v0',
                          params={
                            "client_pool": client_pool,
                            "agent_names" :
                              [
                                "MarLo-Agent-0",
                                "MarLo-Agent-1"
                              ],
                            "comp_all_commands": ["move", "turn", "use"]
                          })

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


for _join_token in join_tokens:
    run_agent(_join_token)


