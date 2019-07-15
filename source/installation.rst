Installation 
============

Using Anaconda_ (**Recommended**)
----------------------------------
  This section assumes that you have Anaconda_ installed.

.. code-block:: bash
 
  conda create python=3.6 --name marlo
  conda config --add channels conda-forge
  conda activate marlo # or `source activate marlo` depending on your conda version
  conda install -c crowdai malmo  
  pip install -U marlo

  # Test installation by :
  python -c "import marlo"
  python -c "from marlo import MalmoPython"

.. _Anaconda: https://www.anaconda.com/download/
.. _here: https://github.com/spMohanty/malmo-conda-recipe

.. Note::
  We support only Anaconda version ``> 4.5.0``. If you have an older anaconda version, please update your conda before proceeding with the installation.


Alternate Approach
---------------------------------------------
  The following section requires you to install the Malmo mod separately via either the PyPi wheel or the latest docker image.
  In order to install Malmo using PyPi, you should:
  
  Install the malmo Python wheel:
    .. code-block:: bash

      pip3 install malmo
  
  Download Malmo into a “MalmoPlatform” directory/folder in your current directory/folder (uses Git)
    .. code-block:: bash

      python3 -c 'import malmo.minecraftbootstrap; malmo.minecraftbootstrap.download()'
 
  Launch one Minecraft instance:
    .. code-block:: bash

      python3 -c 'import malmo.minecraftbootstrap; malmo.minecraftbootstrap.launch_minecraft()'
 
  To set your path from within python assuming that python is running where Malmo was downloaded:
    .. code-block:: bash

      import malmo.minecraftbootstrap; malmo.minecraftbootstrap.set_malmo_xsd_path()

  Following this, you may install the Python binaries for Malmo and the Marlo pack as usual:
  
  .. code-block:: bash

    pip3 install -U marlo
    # Test installation by :
    python3 -c "import marlo"
    python3 -c "from marlo import MalmoPython"
  
  More information can be found under the Marlo documentation:
    https://github.com/Microsoft/malmo/blob/master/scripts/python-wheel/README.md


.. Note::
  If you **did not** install ``marlo`` by using the Anaconda_ package, then you will have 
  to set the ``MALMO_MINECRAFT_ROOT`` environment variable to the absolute path of your 
  Minecraft folder. The ``launchClient.sh`` or ``launchClient.bat`` scripts should be 
  inside this folder.
  You will also have to manually set the ``MALMO_XSD_PATH`` environment variable to 
  the location of your ``Minecraft Schemas`` folder, unless you have done so using the
  bootstrap function provided in the "Alternate Approach" section.
