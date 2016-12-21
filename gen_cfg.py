# -*- coding:utf8 -*-
# File   : gen_cfg.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com 
# 
# This file is part of Atari-Simulator.

import argparse
import gym
import cv2

from asim.utils import scale


def main(args):
    game = gym.make(args.gamename)
    obs = game.reset()
    action_names = game.get_action_meanings()
    action_keys = []

    print('All action names: {}'.format(action_names))
    print('Start recording...')

    cv2.imshow(args.gamename, scale(obs, 600, 800)[:, :, ::-1])
    for i in range(len(action_names)):
        name = action_names[i]
        print('{}-th action, name={}, waiting...'.format(i, name))
        action = cv2.waitKey(0)
        action_keys.append(action)
        print('{}-th action, name={}, key={}, done.'.format(i, name, action))
    print('Recording end.')

    print('Recoding quit action key')
    quit_key = cv2.waitKey(0)
    print('quick action, key={}, done.'.format(quit_key))

    with open(args.cfg, 'w') as f:
        f.write("name = '{}'\n".format(args.gamename))
        f.write("action_names = {}\n".format(repr(action_names)))
        f.write("action_keys = {}\n".format(repr(action_keys)))
        f.write("quit_action_key = {}\n".format(repr(quit_key)))
    print('Cfg file wrtten to {}'.format(args.cfg))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cfg')
    parser.add_argument('gamename')
    main(parser.parse_args())
   
