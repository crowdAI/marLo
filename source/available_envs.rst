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
        .. figure:: https://media.giphy.com/media/u45fNQxG59wfnRpzwJ/giphy.gif
          :align: center
    - **Run the maze!**
        Extra Parameters : 
          - `maze_height` : `2`
        
        More Information : :meth:`marlo.envs.MazeRunner.main`
    

  * - ``MarLo-CliffWalking-v0``
        .. figure:: https://media.giphy.com/media/ef4lPGNqaLlKr45rWB/giphy.gif
          :align: center
    - **Cliff walking mission based on Sutton and Barto**
        
        More Information : :meth:`marlo.envs.CliffWalking.main`


  * - ``MarLo-CatchTheMob-v0``
        .. figure:: https://media.giphy.com/media/9A1gHZrWcaS4AYzcIU/giphy.gif
          :align: center
    - **Catch the Mob**
        
        More Information : :meth:`marlo.envs.CatchTheMob.main`

        
  * - ``MarLo-FindTheGoal-v0``
        .. figure:: https://media.giphy.com/media/1gWkQbDsHOfo4kZXZv/giphy.gif
          :align: center
    - **Find the goal!**
        
        More Information : :meth:`marlo.envs.FindTheGoal.main`


  * - ``MarLo-Attic-v0``
        .. figure:: https://media.giphy.com/media/47C7AYB3FA6kgrMiQ3/giphy.gif
          :align: center
    - **Find the goal! Have you looked in the attic?**
        
        More Information : :meth:`marlo.envs.Attic.main`


  * - ``MarLo-DefaultFlatWorld-v0``
        .. figure:: https://media.giphy.com/media/L0s9QXuR6vIJh6A0dq/giphy.gif
          :align: center
    - **A simple 10 second mission with a reward for reaching a location.**
        
        More Information : :meth:`marlo.envs.DefaultFlatWorld.main`

  * - ``MarLo-DefaultWorld-v0``
        .. figure:: https://media.giphy.com/media/4Nx7gYiM9NDrMrMao7/giphy.gif
          :align: center
    - **Everyday Minecraft life: survival**
        
        More Information : :meth:`marlo.envs.DefaultWorld.main`

  * - ``MarLo-Eating-v0``
        .. figure:: https://media.giphy.com/media/pObNMjjfcGI5tVhmX6/giphy.gif
          :align: center
    - **Healthy diet. Eating right and wrong objects**
        
        More Information : :meth:`marlo.envs.Eating.main`

  * - ``MarLo-Obstacles-v0``
        .. figure:: https://media.giphy.com/media/5sYmFFkq7aEMKTbKP4/giphy.gif
          :align: center
    - **Find the goal! The apartment!**
        
        More Information : :meth:`marlo.envs.Obstacles.main`

  * - ``MarLo-TrickyArena-v0``
        .. figure:: https://media.giphy.com/media/1g1bxw2nD3G9fz2WVV/giphy.gif
          :align: center
    - **Mind your step! Moving around an area to find a goal or get out of it!**
        
        More Information : :meth:`marlo.envs.TrickyArena.main`

  * - ``MarLo-Vertical-v0``
        .. figure:: https://media.giphy.com/media/ZcaMeSnzLrMY1NWM7f/giphy.gif
          :align: center
    - **Find the goal! Without a lift...**

        More Information : :meth:`marlo.envs.Vertical.main`
        
  * - ``MarLo-MobchaseTrainX-v0``
        .. figure:: https://preview.ibb.co/iHKxL0/mobchase.png
          :align: center
    - **Help catch the Mob!MarLo multi-agent missions MobchaseTrain1 to MobchaseTrain5.**

        More Information : :meth:`marlo.envs.MobchaseTrain1.main`

  * - ``MarLo-BuildbattleTrainX-v0``
        .. figure:: https://preview.ibb.co/gb87L0/buildbattle.png
          :align: center
    - **Let's build battle! MarLo multi-agent missions BuildbattleTrain1 to BuildbattleTrain5.** 

        More Information : :meth:`marlo.envs.BuildbattleTrain1.main`

  * - ``MarLo-TreasurehuntTrainX-v0``
        .. figure:: https://preview.ibb.co/gVroSf/treasurehunt.png
          :align: center
    - **Treasure hunting we go! MarLo multi-agent missions TreasurehuntTrain1 to TreasurehuntTrain5.**

        More Information : :meth:`marlo.envs.TreasurehuntTrain1.main`
