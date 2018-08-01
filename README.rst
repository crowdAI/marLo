.. figure:: https://raw.githubusercontent.com/crowdAI/crowdai/master/app/assets/images/misc/crowdai-logo-smile.svg?sanitize=true
  :align: center

MarLÖ : Reinforcement Learning + Minecraft = Awesomeness
============================================================
.. figure:: https://readthedocs.org/projects/marlo/badge/

**MarLÖ** (short for Multi-Agent Reinforcement Learning in MalmÖ) is a high level API built on top of `Project MalmÖ <https://github.com/Microsoft/malmo>`_ to facilitate Reinforcement Learning experiments with a great degree of generalizability, capable of solving problems in pseudo-random, procedurally changing single and multi agent environments withing the world of the mediatic phenomenon game `Minecraft <https://en.wikipedia.org/wiki/Minecraft>`_ .

The `Malmo platform <https://github.com/Microsoft/malmo>`_ provides an API which enables access to actions, observations (i.e. location, surroundings, video frames, game statistics) and other general data that Minecraft provides. Marlo, on the other hand, is a wrapper for Malmo that provides a higher level API and more standardized RL-friendly environment for scientific study.

The framework is written as an extension to `OpenAI's Gym framework <https://github.com/openai/gym>`_
, which is a toolkit for developing and comparing reinforcement learning algorithms, thus providing an industry-standard and familiar platform for scientists, developers and popular RL frameworks.

.. list-table::
  :header-rows: 0
  :widths: 2 2 2
  :align: center
  
  * - ``MarLo-MazeRunner-v0``
        .. figure:: https://i.imgur.com/XpiVIoD.png
          :align: center
          :width: 300    
          
    - ``MarLo-CliffWalking-v0``
        .. figure:: https://i.imgur.com/cI1CgEQ.png
          :align: center
          :width: 300    
          
    - ``MarLo-CatchTheMob-v0``
        .. figure:: https://i.imgur.com/FtfKOzs.png
          :align: center
          :width: 300    

  * - ``MarLo-Basic-v0``
        .. figure:: https://i.imgur.com/lpbQuty.png
          :align: center
          :width: 300    
          
    - ``MarLo-Attic-v0``
        .. figure:: https://imgur.com/fQVuOHD.png
          :align: center
          :width: 300    

    - ``MarLo-DefaultFlatWorld-v0``
        .. figure:: https://i.imgur.com/XQ7UxHP.png
          :align: center
          :width: 300    

  * - ``MarLo-DefaultWorld-v0``
        .. figure:: https://i.imgur.com/bnpM9OX.png
          :align: center
          :width: 300    
          
    - ``MarLo-Eating-v0``
        .. figure:: https://i.imgur.com/kM5Y4pk.png
          :align: center
          :width: 300    

    - ``MarLo-Obstacles-v0``
        .. figure:: https://i.imgur.com/L53AlWG.png
          :align: center
          :width: 300    

  * - ``MarLo-TrickyArena-v0``
        .. figure:: https://i.imgur.com/zfWeCnR.png
          :align: center
          :width: 300    
          
    - ``MarLo-Vertical-v0``
        .. figure:: https://i.imgur.com/jZC7buV.png
          :align: center
          :width: 300    

    - 


Contents
----------------
- `Installation <https://marlo.readthedocs.io/en/latest/installation.html>`_
- `Usage <https://marlo.readthedocs.io/en/latest/usage.html>`_
- `Available Environments <https://marlo.readthedocs.io/en/latest/available_envs.html>`_
- `Submission Instructions <https://marlo.readthedocs.io/en/latest/submit.html>`_
- `Development <https://marlo.readthedocs.io/en/latest/development.html>`_

Simple Example
----------------
.. code-block:: python

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
  

Authors
----------------
- `Sharada Mohanty <https://twitter.com/MeMohanty>`_
