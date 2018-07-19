from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import *  # NOQA
from future import standard_library
standard_library.install_aliases()  # NOQA

import logging
import multiprocessing as mp
import os
import statistics
import time

import numpy as np


"""Columns that describe information about an experiment.

steps: number of time steps taken (= number of actions taken)
episodes: number of episodes finished
elapsed: time elapsed so far (seconds)
mean: mean of returns of evaluation runs
median: median of returns of evaluation runs
stdev: stdev of returns of evaluation runs
max: maximum value of returns of evaluation runs
min: minimum value of returns of evaluation runs
"""
_basic_columns = ('steps', 'episodes', 'elapsed', 'mean',
                  'median', 'stdev', 'max', 'min')


def run_evaluation_episodes(env, agent, n_runs, max_episode_len=None,
                            explorer=None, logger=None):
    """Run multiple evaluation episodes and return returns.

    Args:
        env (Environment): Environment used for evaluation
        agent (Agent): Agent to evaluate.
        n_runs (int): Number of evaluation runs.
        max_episode_len (int or None): If specified, episodes longer than this
            value will be truncated.
        explorer (Explorer): If specified, the given Explorer will be used for
            selecting actions.
        logger (Logger or None): If specified, the given Logger object will be
            used for logging results. If not specified, the default logger of
            this module will be used.
    Returns:
        List of returns of evaluation runs.
    """
    logger = logger or logging.getLogger(__name__)
    scores = []
    print("evaluate " + str(n_runs) + " runs")
    for i in range(n_runs):
        obs = env.reset()
        done = False
        test_r = 0
        t = 0
        while not (done or t == max_episode_len):
            def greedy_action_func():
                return agent.act(obs)
            if explorer is not None:
                a = explorer.select_action(t, greedy_action_func)
            else:
                a = greedy_action_func()
            obs, r, done, info = env.step(a)
            test_r += r
            t += 1
        agent.stop_episode()
        # As mixing float and numpy float causes errors in statistics
        # functions, here every score is cast to float.
        scores.append(float(test_r))
        logger.info('test episode: %s R: %s', i, test_r)
    return scores


def eval_performance(env, agent, n_runs, max_episode_len=None,
                     explorer=None, logger=None):
    """Run multiple evaluation episodes and return statistics.

    Args:
        env (Environment): Environment used for evaluation
        agent (Agent): Agent to evaluate.
        n_runs (int): Number of evaluation runs.
        max_episode_len (int or None): If specified, episodes longer than this
            value will be truncated.
        explorer (Explorer): If specified, the given Explorer will be used for
            selecting actions.
        logger (Logger or None): If specified, the given Logger object will be
            used for logging results. If not specified, the default logger of
            this module will be used.
    Returns:
        Dict of statistics.
    """
    scores = run_evaluation_episodes(
        env, agent, n_runs,
        max_episode_len=max_episode_len,
        explorer=explorer,
        logger=logger)
    stats = dict(
        mean=statistics.mean(scores),
        median=statistics.median(scores),
        stdev=statistics.stdev(scores) if n_runs >= 2 else 0.0,
        max=np.max(scores),
        min=np.min(scores))
    return stats


def record_stats(outdir, values):
    with open(os.path.join(outdir, 'scores.txt'), 'a+') as f:
        print('\t'.join(str(x) for x in values), file=f)


def save_agent(agent, t, outdir, logger, suffix=''):
    dirname = os.path.join(outdir, '{}{}'.format(t, suffix))
    agent.save(dirname)
    logger.info('Saved the agent to %s', dirname)


class Evaluator(object):
    """Object that is responsible for evaluating a given agent.

    Args:
        agent (Agent): Agent to evaluate.
        env (Env): Env to evaluate the agent on.
        n_runs (int): Number of episodes used in each evaluation.
        eval_interval (int): Interval of evaluations in steps.
        outdir (str): Path to a directory to save things.
        max_episode_len (int): Maximum length of episodes used in evaluations.
        explorer (Explorer or None): If set to a Explorer, it is used in
            evaluations. If set to None, actions returned by the agent are
            directly passed to the env.
        step_offset (int): Offset of steps used to schedule evaluations.
        save_best_so_far_agent (bool): If set to True, after each evaluation,
            if the score (= mean of returns in evaluation episodes) exceeds
            the best-so-far score, the current agent is saved.
    """

    def __init__(self,
                 agent,
                 env,
                 n_runs,
                 eval_interval,
                 outdir,
                 max_episode_len=None,
                 explorer=None,
                 step_offset=0,
                 save_best_so_far_agent=True,
                 logger=None,
                 ):
        self.agent = agent
        self.env = env
        self.max_score = np.finfo(np.float32).min
        self.start_time = time.time()
        self.n_runs = n_runs
        self.eval_interval = eval_interval
        self.outdir = outdir
        self.max_episode_len = max_episode_len
        self.explorer = explorer
        self.step_offset = step_offset
        self.prev_eval_t = (self.step_offset -
                            self.step_offset % self.eval_interval)
        self.save_best_so_far_agent = save_best_so_far_agent
        self.logger = logger or logging.getLogger(__name__)

        # Write a header line first
        with open(os.path.join(self.outdir, 'scores.txt'), 'w') as f:
            custom_columns = tuple(t[0] for t in self.agent.get_statistics())
            column_names = _basic_columns + custom_columns
            print('\t'.join(column_names), file=f)

    def evaluate_and_update_max_score(self, t, episodes):
        eval_stats = eval_performance(
            self.env, self.agent, self.n_runs,
            max_episode_len=self.max_episode_len, explorer=self.explorer,
            logger=self.logger)
        elapsed = time.time() - self.start_time
        custom_values = tuple(tup[1] for tup in self.agent.get_statistics())
        mean = eval_stats['mean']
        values = (t,
                  episodes,
                  elapsed,
                  mean,
                  eval_stats['median'],
                  eval_stats['stdev'],
                  eval_stats['max'],
                  eval_stats['min']) + custom_values
        record_stats(self.outdir, values)
        if mean > self.max_score:
            self.logger.info('The best score is updated %s -> %s',
                             self.max_score, mean)
            self.max_score = mean
            if self.save_best_so_far_agent:
                save_agent(self.agent, t, self.outdir, self.logger)
        return mean

    def evaluate_if_necessary(self, t, episodes):
        if t >= self.prev_eval_t + self.eval_interval:
            score = self.evaluate_and_update_max_score(t, episodes)
            self.prev_eval_t = t - t % self.eval_interval
            return True, score
        return False, None

