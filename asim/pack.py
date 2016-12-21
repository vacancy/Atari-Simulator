# -*- coding:utf8 -*-
# File   : pack.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com 
# 
# This file is part of Atari-Simulator.

from .utils import module_vars_as_dict


class Pack(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.steps = []
        self.is_ended = False

        self.__last_observation = None

    def reset(self, observation):
        self.__last_observation = observation

    def step(self, action, observation, reward, done, info):
        assert not self.is_ended

        last_observation = self.__last_observation

        if done:
            self.is_ended = True
            self.__last_observation = None
        else:
            self.__last_observation = observation

        record = dict(
            action=action,
            observation=last_observation,
            reward=reward,
            info=info)
        self.steps.append(record)

    def make_pickleable(self):
        return dict(
            cfg=module_vars_as_dict(self.cfg),
            steps=self.steps,
            is_ended=self.is_ended
        )

