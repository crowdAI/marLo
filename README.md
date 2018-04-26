# marLo

**marLo : Multi Agent Reinforcement Learning using [MalmÖ](https://github.com/Microsoft/malmo)**

# Usage
```python
import marlo
env = marlo.make('marlo-nips2018-env01')
env.init()
observation = env.reset()

for _ in range(1000):
  env.render()
  action = env.action_space.sample() # take a random action
  observation, reward, done, info = env.step(action)
  if done:
    break
```

# Authors
S.P. Mohanty (<sharada.mohanty@epfl.ch>)   
**...you could be next...**
