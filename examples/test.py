import marlo
import time
# Ensure that you have a minecraft-client running with : marlo-server --port 10000
join_tokens = marlo.make('MazeRunner-v0',
                 params={
                    "videoResolution" : [800, 600],
                    "client_pool" : [("127.0.0.1", 10000)],
                    "forceWorldReset" : True,
                    "allowContinuousMovement" : ["move", "turn"],
                    "continuous_discrete": True
                 })

# env, join_tokens = marlo.make("/Users/spmohanty/work/marlo/marlo-py/marlo/assets/mob_chase.xml", 
#                  params={
#                     "videoResolution" : [800, 600],
#                     "client_pool" : [("127.0.0.1", 10000), ("127.0.0.1", 10001)],
#                     "forceWorldReset" : True,
#                     "allowContinuousMovement" : ["move", "turn"],
#                     "continuous_discrete": True
#                  })

print(join_tokens)

# frame = env.reset()
# print(frame.shape)
# print(env.action_names)
# import json
# print(json.dumps(env.params, indent=4))
# 
# 
env = marlo.init(join_tokens[0])
frame = env.reset()
print(frame.shape)
print(env.action_names)
import json
print(json.dumps(env.params, indent=4))
# 
# 
done = False
while not done:
    _action = env.action_space.sample()
    obs, reward, done, info = env.step(env.action_space.sample())
    time.sleep(0.5)
    print("reward:", reward)
    # print("done:", done)
    # print("info", info)    
# 

#TODO marlo.make('env_name') # return a gym environment

# env.init(
#     videoResolution=[800, 600]
#     )
# # List of all available options at : https://github.com/spMohanty/marLo/blob/dev/docs/init.md
# 
# for _ in range(10):
#     t = time.time()
#     env.reset()
#     t2 = time.time()
#     print("Startup time:", t2 - t)
#     done = False
#     s = 0
#     while not done:
#         obs, reward, done, info = env.step(env.action_space.sample())
#         env.render()
#         #print("obs:", obs.shape)
#         #print("reward:", reward)
#         #print("done:", done)
#         #print("info", info)
#         s += 1
#     t3 = time.time()
#     print((t3 - t2), "seconds total,", s, "steps total,", s / (t3 - t2), "steps/second")
