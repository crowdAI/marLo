Installation 
============

Using Anaconda_ (Only for `linux` and `osx`)
---------------------------------------------
  This section assumes that you are on ``linux`` or ``osx`` and have Anaconda_ installed.

.. code-block:: bash
 
  conda create python=3.6 --name marlo
  conda config --add channels conda-forge
  conda activate marlo # or `source activate marlo` depending on your conda version
  conda install -c crowdai malmo  
  pip install -U marlo

  # Test installation by :
  python -c "import marlo"
  python -c "from marlo import MalmoPython"

.. Note::
  **Help Wanted** : The conda recipes used to build this conda package can be found here_ . We do not yet have a Windows build, and hence pull requests adding a windows build are very welcome.

.. _Anaconda: https://www.anaconda.com/download/
.. _here: https://github.com/spMohanty/malmo-conda-recipe



On  Windows
---------------------------------------------
.. code-block:: bash

  pip3 install -U malmo
  pip3 install -U marlo
  # Test installation by :
  python3 -c "import marlo"
  python3 -c "from marlo import MalmoPython"


.. Note::
  If you **did not** install ``marlo`` by using the Anaconda_ package, then you will have 
  to set the ``MALMO_MINECRAFT_ROOT`` environment variable to the absolute path of your 
  Minecraft folder. The ``launchClient.sh`` or ``launchClient.bat`` scripts should be 
  inside this folder.
  You will also have to manually set the ``MALMO_XSD_PATH`` environment variable to 
  the location of your ``Minecraft Schemas`` folder.
