# -*- coding:utf8 -*-
# File   : main.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com 
# 
# This file is part of Atari-Simulator.

import argparse
import pickle
import time
import threading
import gym
import cv2
import os.path as osp

from asim.controller import Controller
from asim.utils import load_module_filename, scale
from asim.pack import Pack 

__quit_action__ = 32767
__window_size__ = (600, 800)


def vis_and_action(args, cfg, controller, observation):
    display = scale(observation, *__window_size__)
    controller.update(display)
  
    action = 0
    for i in reversed(range(len(cfg.action_keys))):
        if controller.test_key(cfg.action_keys[i]): 
            print('action: {}'.format(cfg.action_names[i]))
            action = i
            break

    if controller.test_key(cfg.quit_action_key):
        action = __quit_action__

    time.sleep((1.0/ args.fps))

    return action


def dump_pack(cfg, pack):
    pickleable = pack.make_pickleable()

    name = cfg.name + '-'
    name += time.strftime('%Y%m%d-%H%M%S')
    name += '.replay.pkl'
    with open(osp.join('replays', name), 'wb') as f:
        pickle.dump(pickleable, f, pickle.HIGHEST_PROTOCOL)
    print('replay written to replays/{}'.format(name))


def main(args, controller):
    cfg = load_module_filename(args.cfg)
    pack = Pack(cfg)

    controller.update_title(cfg.name)
    game = gym.make(cfg.name)
    obs = game.reset()
    pack.reset(obs)
   
    while not pack.is_ended:
        action = vis_and_action(args, cfg, controller, obs)
        if action == __quit_action__:
            break

        res = game.step(action)
        obs = res[0]
        pack.step(action, *res)

    dump_pack(cfg, pack)
    from IPython import embed; embed()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cfg')
    parser.add_argument('-fps', '--fps', dest='fps', default=24, type=int)
    parser.add_argument('-sfps', '--screen-fps', dest='sfps', default=100, type=int)
    
    controller = Controller()
    thread = threading.Thread(target=main, args=(parser.parse_args(), controller))

    thread.start()
    controller.mainloop()
  
