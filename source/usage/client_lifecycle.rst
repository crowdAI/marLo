Client Lifecycle (experimental)
===================================

In the examples above, we manually start the `client_pools` by running something along the lines of : 

.. code-block:: bash

  $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000
  $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10001
  
  
An experimental feature also allows you to start the ``launchClients`` on the fly.
The cleanup of the said Minecraft client processes is still not done automatically and the users are expected 
to manually remove the said clients when they are done. (This will change soon.)

This can be achieved by two ways : 

1) **Automatically**

If the ``game_params`` provided to ``marlo.make`` do not contain the ``client_pool`` key, then ``marlo`` will attempt to start the correct number of clients on some random free ports.
 
.. code-block:: python


  import marlo
  join_tokens = marlo.make('MarLo-MazeRunner-v0', 
                            params={
                              "agent_names" : 
                                [
                                  "MarLo-Agent-0", 
                                  "MarLo-Agent-1"
                                ]
                            })

The code above should automatically start two Minecraft clients. 

2) **Manual Launch**

.. code-block:: python

  import marlo
  client_pool = marlo.launch_clients(2)
  join_tokens = marlo.make('MarLo-MazeRunner-v0', 
                            params={
                              "client_pool" : client_pool,
                              "agent_names" : ["MarLo-Agent-0", "MarLo-Agent-1"]
                            })

  The ``marlo.launch_clients`` helper function will launch the clients.

|

.. warning::
  **The Minecraft Client processes created by this approach are not automatically cleaned up.**

.. note::
  - Both the approaches above expect the ``MALMO_MINECRAFT_ROOT`` environment variable to point to the absolute path of the Minecraft folder containing the ``launchClient`` scripts.
