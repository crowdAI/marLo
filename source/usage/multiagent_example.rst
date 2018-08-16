Multi Agent Example
=====================

.. image:: https://i.imgur.com/mlF3X0M.png

In a Multi Agent setup, the number of agents is estimated from the list of 
``agent_names`` passed as a param to ``marlo.make``. Then marlo returns ``join_tokens``
for all the agents in the specified game as a list. Then ``marlo.init`` can be used to 
join the game as separate agents.

- **Start Minecraft Clients**

.. code-block:: bash

  $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000
  $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10001

  .. Note:: 
      In case of ``Windows``, you can instead use |
      ``cd %MALMO_MINECRAFT_ROOT`` |
      ``launchClient.bat`` |  

- **Create Game**

.. code-block:: python
  :linenos:

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

.. Note:: 
  For the curious, the ``params`` object provided to the ``marlo.make`` and ``marlo.init`` can have the values described in :meth:`marlo.base_env_builder.MarloEnvBuilderBase.default_base_params`


- **Define a function for running a single Agent**

.. code-block:: python
  :lineno-start: 15

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

.. Note:: 
  Notice the ``@marlo.threaded`` decorator, which just runs the given function in a separate thread.

- **Run both the Agents**

.. code-block:: python
  :lineno-start: 28

  # Run agent-0
  thread_handler_0, _ = run_agent(join_tokens[0])
  # Run agent-1
  thread_handler_1, _ = run_agent(join_tokens[1])

  # Wait for both the threads to complete execution
  thread_handler_0.join()
  thread_handler_1.join()

  print("Episode Run Complete")

Example Code
-------------

.. code-block:: python
  :linenos:
  
  #!/usr/bin/env python
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
  
  # Wait for both the threads to complete execution
  thread_handler_0.join()
  thread_handler_1.join()
  
  print("Episode Run Complete")
