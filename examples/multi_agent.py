#!/usr/bin/env python
# Please ensure that you have two Minecraft clients running on port 10000 and 
# port 10001 by doing : 
# $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000
# $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10001

import marlo
client_pool = [('127.0.0.1', 10000),('127.0.0.1', 10001)]
join_tokens = marlo.make('MarLo-MazeRunner-v0',
                          params={
                            "client_pool": client_pool,
                            "agent_names" :
                              [
                                "MarLo-Agent-0",
                                "MarLo-Agent-1"
                              ]
                          })
# As this is a two-agent scenario,
# there will just two join tokens
assert len(join_tokens) == 2

@marlo.threaded
def run_agent(join_token):
    env = marlo.init(join_token)
    observation = env.reset()
    done = False
    count = 0
    while not done:
        _action = env.action_space.sample()
        obs, reward, done, info = env.step(_action)
        print("reward:", reward)
        print("done:", done)
        print("info", info)
    env.close()

# Run agent-0
thread_handler_0, _ = run_agent(join_tokens[0])
# Run agent-1
thread_handler_1, _ = run_agent(join_tokens[1])

# Wait until Both the threads complete execution
thread_handler_0.join()
thread_handler_1.join()

print("Episode Run complete")
