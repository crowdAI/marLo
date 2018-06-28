import gym
import marlo

env = gym.make('MinecraftBasic-v0')
# Ensure you have minecraft clients running with :
# malmo-server --port 10000
# malmo-server --port 10001
# malmo-server --port 10002
env.init(client_pool=[("localhost", 10000), ("localhost", 10001), ("localhost", 10002)])
# List of all available options at : https://github.com/spMohanty/marLo/blob/dev/docs/init.md
env.reset()

done = False
while not done:
    env.render()
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
