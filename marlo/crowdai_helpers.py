#!/usr/bin/env python
import os
import crowdai_api


class CrowdAIMarloEvents:
    REQUEST_ENV_JOIN_TOKENS="marlo.events.REQUEST_JOIN_TOKENS"
    ENV_JOIN_TOKENS="marlo.events.JOIN_TOKENS"
    END_OF_GRADING="marlo.events.END_OF_GRADING"

    GAME_INIT="marlo.events.GAME_INIT"
    ENV_RESET="marlo.events.ENV_RESET"
    ENV_ACTION="marlo.events.ENV_ACTION"
    STEP_REWARD="marlo.events.STEP_REWARD"
    
def is_grading():
    """Returns if the code is being executed inside the crowdAI evaluation 
    system.

    :returns: Boolean
    """
    return os.getenv("CROWDAI_IS_GRADING", False)

def evaluator_join_token(params={}):
    """Returns evaluator join tokens from the crowdAI evaluation system
    
    :param params: a dictionary containing game params. Note that only a certain 
                subset of params will be considered by the grader. TODO: Add list
    :type params: dict
    
    :returns: a list of strings representing join tokens for all the agents 
              in a game; or marks the end of the evaluation

    """
    crowdai_events = crowdai_api.CrowdAIEvents()
    # Request a list of JOIN_TOKENS
    response = crowdai_events.register_event(
        event_type=CrowdAIMarloEvents.REQUEST_ENV_JOIN_TOKENS,
        message="",
        payload={"params": params},
        blocking=True
        )
    if not response:
        register_end_of_grading(crowdai_events)

    return response

def register_end_of_grading(crowdai_events):
    """Marks the end of an evaluation, and waits for the rest of the 
    evaluation system to complete the post processing.

    :param crowdai_events: a crowdai events object
    :type `crowdai_api.CrowdAIEvents` object

    """
    crowdai_events.register_event(
        event_type=CrowdAIMarloEvents.END_OF_GRADING,
        message="",
        payload={},
        blocking=True
        )

class CrowdAiNotifier():
    @staticmethod
    def _send_notification(event_type, message, payload={}, blocking=False):
        crowdai_events = crowdai_api.events.CrowdAIEvents()
        default_payload = {"challenge_id": "NIPS18_AVC"}
        default_payload.update(payload)
        crowdai_events.register_event(event_type, message, payload, blocking)

    @staticmethod
    def _game_init():
        CrowdAiNotifier._send_notification(
            event_type=CrowdAIMarloEvents.GAME_INIT,
            message={},
            payload={},
            blocking=False)

    @staticmethod
    def _env_reset():
        CrowdAiNotifier._send_notification(
            event_type=CrowdAIMarloEvents.ENV_RESET,
            message={},
            payload={},
            blocking=False)

    @staticmethod
    def _env_action(action):
        CrowdAiNotifier._send_notification(
            event_type=CrowdAIMarloEvents.ENV_ACTION,
            message={},
            payload={"action": action},
            blocking=False)


    @staticmethod
    def _step_reward(reward):
        CrowdAiNotifier._send_notification(
            event_type=CrowdAIMarloEvents.STEP_REWARD,
            message={},
            payload={"r":reward},
            blocking=False)
