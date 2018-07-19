# Available Envs
* MinecraftDefaultWorld1-v0
* MinecraftDefaultFlat1-v0
* MinecraftTrickyArena1-v0
* MinecraftEating1-v0
* MinecraftCliffWalking1-v0
* MinecraftMaze1-v0
* MinecraftMaze2-v0
* MinecraftBasic-v0
* MinecraftObstacles-v0
* MinecraftSimpleRoomMaze-v0
* MinecraftAttic-v0
* MinecraftVertical-v0
* MinecraftComplexityUsage-v0
* MinecraftMedium-v0
* MinecraftHard-v0
* minecraft
* MinecraftDefaultWorld1-v0
* MinecraftDefaultFlat1-v0
* CatchTheMobSinglePlayer-v0

You can use these by
```python
import gym
import marlo
gym.make("<env_name>")
env.init()

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
        #print "obs:", obs.shape
        #print "reward:", reward
        #print "done:", done
        #print "info", info
        s += 1
    t3 = time.time()
    print((t3 - t2), "seconds total,", s, "steps total,", s / (t3 - t2), "steps/second")
```
