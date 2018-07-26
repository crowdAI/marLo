import gym
import marlo
import time

# Ensure that you have a minecraft-client running with : marlo-server --port 10000
env = gym.make('MinecraftBasic-v0')
#TODO marlo.make('env_name') # return a gym environment

env.init(
    videoResolution=[800, 600]
    )
# List of all available options at : https://github.com/spMohanty/marLo/blob/dev/docs/init.md

for _ in range(10):
    t = time.time()
    env.reset()
    t2 = time.time()
    print("Startup time:", t2 - t)
    done = False
    s = 0
    while not done:
        obs, reward, done, info = env.step(env.action_space.sample())
        env.render()
        #print("obs:", obs.shape)
        #print("reward:", reward)
        #print("done:", done)
        #print("info", info)
        s += 1
    t3 = time.time()
    print((t3 - t2), "seconds total,", s, "steps total,", s / (t3 - t2), "steps/second")
