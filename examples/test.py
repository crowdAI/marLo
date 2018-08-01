import marlo
import time
import json
import base64

client_pool = [('127.0.0.1', 10000)]
join_tokens = marlo.make('MarLo-MazeRunner-v0',
                 params={
                    "videoResolution" : [800, 600],
                    "client_pool" : client_pool,
                    "agent_names" : ["MarLo-Agent0"],
                    "allowContinuousMovement" : ["move", "turn"],
                 })

def run_agent(join_token):
    env = marlo.init(join_token)
    frame = env.reset()
    done = False
    count = 0
    while not done:
        _action = env.action_space.sample()
        # obs, reward, done, info = env.step(_action)
        time.sleep(0.5)
        # print("reward:", reward)
        # print("done:", done)
        # print("info", info)
    env.close()

for _join_token in join_tokens:
    run_agent(_join_token)
