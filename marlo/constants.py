"""
submodule holding all marlo constants.

Currently includes :


.. code-block:: python

    JOIN_WHITELISTED_PARAMS = [
        "videoResolution",
        "recordMP4",
        "recordCommands",
        "recordRewards",
        "recordObservations",
        "recordDestination",
        "seed"
    ]
    SINGLE_DIRECTION_DISCRETE_MOVEMENTS = \
                [
                    "jumpeast", "jumpnorth", "jumpsouth", "jumpwest",
                    "movenorth", "moveeast", "movesouth", "movewest",
                    "jumpuse", "use", "attack", "jump"
                ]
    MULTIPLE_DIRECTION_DISCRETE_MOVEMENTS = \
            [
                "move", "turn", "look", "strafe", "jumpmove", 
                "jumpstrafe"
            ]

"""

JOIN_WHITELISTED_PARAMS = [
    "videoResolution",
    "recordMP4",
    "recordCommands",
    "recordRewards",
    "recordObservations",
    "recordDestination",
    "seed"
]


SINGLE_DIRECTION_DISCRETE_MOVEMENTS = \
            [
                "jumpeast", "jumpnorth", "jumpsouth", "jumpwest",
                "movenorth", "moveeast", "movesouth", "movewest",
                "jumpuse", "use", "attack", "jump"
            ]
MULTIPLE_DIRECTION_DISCRETE_MOVEMENTS = \
            [
                "move", "turn", "look", "strafe", "jumpmove", 
                "jumpstrafe"
            ]
