import marlo
import time
import json
import base64

client_pool = [('127.0.0.1', 10000), ('127.0.0.1', 10001)]
join_tokens = marlo.make('MarLo-MazeRunner-v0',
                 params={
                    "agent_names" : ["MarLo-Agent0"],
                    "videoResolution" : [800, 600],
                    "forceWorldReset" : True,
                    "client_pool" : client_pool,
                    "allowContinuousMovement" : ["move", "turn"],
                    "recordMP4" : "video"
                 })


@marlo.threaded
def run_agent(join_token):
    env = marlo.init(join_token)
    frame = env.reset()
    done = False
    while not done:
        _action = env.action_space.sample()
        obs, reward, done, info = env.step(_action)
        time.sleep(0.5)
        print("reward:", reward)
        print("done:", done)
        print("info", info)


for _join_token in join_tokens:
    run_agent(_join_token)
