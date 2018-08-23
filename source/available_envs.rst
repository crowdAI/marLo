Available Environments
==============================

.. Note::
  All the environments will have access to the default game parameters (as described in :meth:`marlo.base_env_builder.MarloEnvBuilderBase.default_base_params`), and apart from that some of them might expose some extra parameters which will be listed here.


.. tabularcolumns:: | screenshot | id | description |

.. list-table::
  :header-rows: 1
  :widths: 3 3
  

  * - 
    - **Description**

  * - ``MarLo-MazeRunner-v0``
        .. figure:: https://media.giphy.com/media/X7rQC4iIV2jM9ti7wb/giphy.gif
          :align: center
    - **Run the maze!**
        Extra Parameters : 
          - `maze_height` : `2`
        
        More Information : :meth:`marlo.envs.MazeRunner.main`
    

  * - ``MarLo-CliffWalking-v0``
        .. figure:: https://media.giphy.com/media/4ahHkEvQ5gdpg5y3gq/giphy.gif
          :align: center
    - **Cliff walking mission based on Sutton and Barto**
        
        More Information : :meth:`marlo.envs.CliffWalking.main`


  * - ``MarLo-CatchTheMob-v0``
        .. figure:: https://media.giphy.com/media/8FiMcxgnZhpt9u1ZD2/giphy.gif
          :align: center
    - **Catch the Mob**
        
        More Information : :meth:`marlo.envs.CatchTheMob.main`

        
  * - ``MarLo-FindTheGoal-v0``
        .. figure:: https://media.giphy.com/media/azHZmMl2fl2xBKPqAB/giphy.gif
          :align: center
    - **Find the goal!**
        
        More Information : :meth:`marlo.envs.Basic.main`


  * - ``MarLo-Attic-v0``
        .. figure:: https://media.giphy.com/media/2Y9MXD4knMrBGnXASL/giphy.gif
          :align: center
    - **Find the goal! Have you looked in the attic?**
        
        More Information : :meth:`marlo.envs.Attic.main`


  * - ``MarLo-DefaultFlatWorld-v0``
        .. figure:: https://media.giphy.com/media/t6Kf1RcIqr3UxEmNRz/giphy.gif
          :align: center
    - **A simple 10 second mission with a reward for reaching a location.**
        
        More Information : :meth:`marlo.envs.DefaultFlatWorld.main`

  * - ``MarLo-DefaultWorld-v0``
        .. figure:: https://media.giphy.com/media/wHencJtdUw9sBCcKxs/giphy.gif
          :align: center
    - **Everyday Minecraft life: survival**
        
        More Information : :meth:`marlo.envs.DefaultWorld.main`

  * - ``MarLo-Eating-v0``
        .. figure:: https://media.giphy.com/media/3q0wQ72sd54VaEc0AI/giphy.gif
          :align: center
    - **Healthy diet. Eating right and wrong objects**
        
        More Information : :meth:`marlo.envs.Eating.main`

  * - ``MarLo-Obstacles-v0``
        .. figure:: https://media.giphy.com/media/F14vxiNDfTjF8wyJfH/giphy.gif
          :align: center
    - **Find the goal! The apartment!**
        
        More Information : :meth:`marlo.envs.Obstacles.main`

  * - ``MarLo-TrickyArena-v0``
        .. figure:: https://media.giphy.com/media/7zuPK2Fu5uyslCCGjY/giphy.gif
          :align: center
    - **Mind your step! Moving around an area to find a goal or get out of it!**
        
        More Information : :meth:`marlo.envs.TrickyArena.main`

  * - ``MarLo-Vertical-v0``
        .. figure:: https://media.giphy.com/media/2Y9MXD4knMrBGnXASL/giphy.gif
          :align: center
    - **Find the goal! Without a lift...**
        
        More Information : :meth:`marlo.envs.Vertical.main`
