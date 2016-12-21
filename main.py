# -*- coding:utf8 -*-
# File   : main.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com 
# 
# This file is part of Atari-Simulator.

import argparse
import pickle
import time
import gym
import cv2
import os.path as osp

from asim.utils import load_module_filename, scale
from asim.pack import Pack 

__quit_action__ = 32767

def vis_and_action(args, cfg, observation):
    display = scale(observation, 600, 800)[:, :, ::-1]
    cv2.imshow(cfg.name, display)
   
    # while True:
    if True:
        action = cv2.waitKey(int(1000 / args.fps))
        for i in range(len(cfg.action_keys)):
            if action == cfg.action_keys[i]:
                print('action: {}'.format(cfg.action_names[i]))
                return i
        if action == cfg.quit_action_key:
            return __quit_action__
        print('invalid action: {}'.format(action))
        return 0

def dump_pack(cfg, pack):
    pickleable = pack.make_pickleable()

    name = cfg.name + '-'
    name += time.strftime('%Y%m%d-%H%M%S')
    name += '.replay.pkl'
    with open(osp.join('replays', name), 'wb') as f:
        pickle.dump(pickleable, f, pickle.HIGHEST_PROTOCOL)
    print('replay written to replays/{}'.format(name))


def main(args):
    cfg = load_module_filename(args.cfg)
    pack = Pack(cfg)

    game = gym.make(cfg.name)
    obs = game.reset()
    pack.reset(obs)
   
    while not pack.is_ended:
        action = vis_and_action(args, cfg, obs)
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
    parser.add_argument('-fps', '--fps', dest='fps', default=24)
    main(parser.parse_args())
    
