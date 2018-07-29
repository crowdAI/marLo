Usage
=====

Basic Usage
-----------

- **Start Minecraft Clients**

.. code-block:: bash

  $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000

**Note** : In case of ``Windows``, you can use ``%%MALMO_MINECRAFT_ROOT%%`` instead.


- **Make and Instantiate Environment**

.. code-block:: python
  
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

- **Get first Observation**

.. code-block:: python
  
  observation = env.reset()

- **Start Game Loop**

.. code-block:: python
  
  done = False
  while not done:
    _action = env.action_space.sample()
    obs, reward, done, info = env.step(_action)
    print("reward:", reward)
    print("done:", done)
    print("info", info)
  env.close()


Multi Agent Example
-------------------

- **Start Minecraft Clients**

.. code-block:: bash

  $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000
  $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10001

**Note** : In case of ``Windows``, you can use ``%%MALMO_MINECRAFT_ROOT%%`` instead.
  

- **Create Game**

.. code-block:: python

  import marlo
  client_pool = [('127.0.0.1', 10000),('127.0.0.1', 10001)]
  join_tokens = marlo.make('MarLo-MazeRunner-v0', 
                            params={
                              "client_pool": client_pool,
                              "agent_names" : ["MarLo-Agent-0", "MarLo-Agent-1"]
                            })
  # As this is a two-agent scenario, 
  # there will just two join tokens
  assert len(join_tokens) == 2
  
- **Define a function for running a single Agent**

.. code-block:: python

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

**Note** : Notice the ``@marlo.threaded`` decorator, which jus runs the given 
function in a separate thread.

- Run both the Agents

.. code-block:: python

  # Run agent-0
  run_agent(join_tokens[0])
  run_agent(join_tokens[1])
  
