Installation 
============

Using Anaconda_ (Only for `linux` and `osx`)
---------------------------------------------
  This section assumes that you are only on ``linux`` or ``osx`` and have Anaconda_ installed.

.. code-block:: bash
 
  conda create python=3.6 --name marlo
  conda install -c crowdai malmo
  conda activate malmo
  pip install -U marlo

  # Test installation by :
  python -c "import marlo"
  python -c "import marlo.MalmoPython"

.. Note::
  **Help Wanted** : The conda recipes used to build this conda package can be found here_ . Pull requests adding a windows build are very welcome.

.. _Anaconda: https://www.anaconda.com/download/
.. _here: https://github.com/spMohanty/malmo-conda-recipe



On  Windows
---------------------------------------------
.. code-block:: bash

  pip3 install -U malmo
  pip3 install -U marlo
  # Test installation by :
  python -c "import marlo"
  python -c "import marlo.MalmoPython"


|
|

**Note :** If you **did not** install ``marlo`` by using the Anaconda_ package, then you will have 
to set the ``MALMO_MINECRAFT_ROOT`` environment variable to the absolute path of your 
Minecraft folder. The ``launchClient.sh`` or ``launchClient.bat`` scripts should be 
inside this folder.
