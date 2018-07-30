.. figure:: https://raw.githubusercontent.com/crowdAI/crowdai/master/app/assets/images/misc/crowdai-logo-smile.svg?sanitize=true
  :align: center

MarLÖ
======

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


Contents
--------

- Installation 
- Usage
- Game Variables
- Available Environments
- Submission Instructions

Authors
========
- `Sharada Mohanty <https://twitter.com/MeMohanty>`_
