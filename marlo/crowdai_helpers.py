#!/usr/bin/env python
import os
import crowdai_api

########################################################################
# Instatiate Event Notifier
########################################################################
crowdai_events = crowdai_api.events.CrowdAIEvents()

class CrowdAIMarloEvents:
    REQUEST_ENV_JOIN_TOKENS="marlo.events.REQUEST_JOIN_TOKENS"
    END_OF_GRADING="marlo.events.END_OF_GRADING"

    GAME_INIT="marlo.events.GAME_INIT"
    ENV_RESET="marlo.events.ENV_RESET"
    ENV_ACTION="marlo.events.ENV_ACTION"
    STEP_REWARD="marlo.events.STEP_REWARD"
    
    EPISODE_PENDING="marlo.events.EPISODE_PENDING"
    EPISODE_INITIATED="marlo.events.EPISODE_INITIATED"
    EPISODE_RUNNING="marlo.events.EPISODE_RUNNING"
    EPISODE_DONE="marlo.events.EPISODE_DONE" #Episode Complete
    EPISODE_ERROR="marlo.events.EPISODE_ERROR"
    
    EVALUATION_PENDING="marlo.events.EVALUATION_PENDING"
    EVALUATION_RUNNING="marlo.events.EVALUATION_RUNNING"
    EVALUATION_ERROR="marlo.events.EVALUATION_ERROR"
    EVALUATION_COMPLETE="marlo.events.EVALUATION_COMPLETE"

def is_grading():
    """Returns if the code is being executed inside the crowdAI evaluation 
    system.

    :returns: bool
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
        event_type=crowdai_events.CROWDAI_EVENT_INFO,
        message="",
        payload={
            "event_type": CrowdAIMarloEvents.REQUEST_ENV_JOIN_TOKENS,
            "params": params
            },
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
        event_type=crowdai_events.CROWDAI_EVENT_INFO,
        message="",
        payload={
            "event_type": CrowdAIMarloEvents.END_OF_GRADING
        },
        blocking=True
        )

class CrowdAiNotifier():
    @staticmethod
    def _send_notification(event_type, message, payload={}, blocking=False):
        crowdai_events = crowdai_api.events.CrowdAIEvents()
        default_payload = {"challenge_id": "MarLo"}
        default_payload.update(payload)
        crowdai_events.register_event(event_type, message, payload, blocking)

    @staticmethod
    def _game_init():
        CrowdAiNotifier._send_notification(
            event_type=crowdai_events.CROWDAI_EVENT_INFO,
            message="Game Initialized",
            payload={
                "event_type" : CrowdAIMarloEvents.GAME_INIT
            },
            blocking=False)

    @staticmethod
    def _env_reset():
        CrowdAiNotifier._send_notification(
            event_type=crowdai_events.CROWDAI_EVENT_INFO,
            message="Environment Reset",
            payload={
                "event_type" : CrowdAIMarloEvents.ENV_RESET
            },
            blocking=False)

    @staticmethod
    def _env_action(action):
        CrowdAiNotifier._send_notification(
            event_type=crowdai_events.CROWDAI_EVENT_INFO,
            message="",
            payload={
                "event_type" : CrowdAIMarloEvents.ENV_ACTION,
                "action": action
            },
            blocking=False)


    @staticmethod
    def _step_reward(reward):
        CrowdAiNotifier._send_notification(
            event_type=crowdai_events.CROWDAI_EVENT_INFO,
            message="",
            payload={
                    "event_type" : CrowdAIMarloEvents.STEP_REWARD,
                    "r":reward
                },
            blocking=False)

    @staticmethod
    def _episode_done():
        CrowdAiNotifier._send_notification(
            event_type=crowdai_events.CROWDAI_EVENT_INFO,
            message="",
            payload={
                    "event_type" : CrowdAIMarloEvents.EPISODE_DONE,
                },
            blocking=False)

    
    @staticmethod
    def _env_error(error_message):
        CrowdAiNotifier._send_notification(
            event_type=crowdai_events.CROWDAI_EVENT_ERROR,
            message="execution_error",
            payload={
                    "event_type" : CrowdAIMarloEvents.EPISODE_ERROR,
                    "error_message":error_message
                },
            blocking=False)
