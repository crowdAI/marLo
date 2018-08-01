#!/usr/bin/env python
# Please ensure that you have a Minecraft client running on port 10000
# by doing : 
# $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000


import marlo
client_pool = [('127.0.0.1', 10000)]
join_tokens = marlo.make('MarLo-MazeRunner-v0',
                          params={
                            "client_pool": client_pool
                          })
# As this is a single agent scenario,
# there will just be a single token
assert len(join_tokens) == 1
join_token = join_tokens[0]

env = marlo.init(join_token)

observation = env.reset()

done = False
while not done:
    _action = env.action_space.sample()
    obs, reward, done, info = env.step(_action)
    print("reward:", reward)
    print("done:", done)
    print("info", info)
env.close()
