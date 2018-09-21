Single Agent Example
======================

In the simplest of the use cases, we will start a single agent 
**Marlo** environment, and connect an agent to the environment and take some 
*random actions*.

.. image:: https://i.imgur.com/XpiVIoD.png
  

- **Start Minecraft Clients**

.. code-block:: bash

  $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000

.. Note:: 
    In case of ``Windows``, you can instead use |
    ``cd %MALMO_MINECRAFT_ROOT%`` |
    ``launchClient.bat`` |

- **Make and Instantiate Environment**

.. code-block:: python
  :linenos:
  
  import marlo
  client_pool = [('127.0.0.1', 10000)]
  join_tokens = marlo.make('MarLo-FindTheGoal-v0', 
                            params={
                              "client_pool": client_pool
                            })
  # As this is a single agent scenario, 
  # there will just be a single token
  assert len(join_tokens) == 1
  join_token = join_tokens[0]
  
  env = marlo.init(join_token)
  
.. Note:: 
  For the curious, the ``params`` object provided to the ``marlo.make`` and ``marlo.init`` can have the values described in :meth:`marlo.base_env_builder.MarloEnvBuilderBase.default_base_params`

- **Get first Observation**

.. code-block:: python
  :lineno-start: 13
  
  observation = env.reset()

- **Start Game Loop**

.. code-block:: python
  :lineno-start: 14
  
  done = False
  while not done:
    _action = env.action_space.sample()
    obs, reward, done, info = env.step(_action)
    print("reward:", reward)
    print("done:", done)
    print("info", info)
  env.close()
  
Example Code
-------------

.. code-block:: python
  :linenos:
  
  #!/usr/bin/env python
  # $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000  
  
  import marlo
  client_pool = [('127.0.0.1', 10000)]
  join_tokens = marlo.make('MarLo-FindTheGoal-v0', 
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
  
  
