# Marlo

**marLo : Multi Agent Reinforcement Learning using [MalmÖ](https://github.com/Microsoft/malmo)**

Check the MARLO documentation at our [Wiki](https://github.com/crowdAI/marLo/wiki) 

```python
import marlo
env, join_tokens = marlo.make("Maze-Runner-v0", params={
  videoResolution=[800, 600]
})
# * marlo.make supports ALL parameters
# * marlo.join supports a subset of parameters

# env.init(params=dict(
#   videoResolution=[800, 600]
# ))
# This joins as role 0

# For other agents. They can join as : 
import marlo
join_tokens = json.dumps(dict(
  params={},
  role=1,
  experiment_id="something"#compute dynamically
))
env = marlo.join_game(env_string)

# Then both can do :
  env.step
  env.reset
  env.action_space
  etc
```
