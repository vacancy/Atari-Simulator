# -*- coding:utf8 -*-
# File   : gen_cfg.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com 
# 
# This file is part of Atari-Simulator.

import argparse
import gym
import cv2
import threading
from PIL import Image

from asim.controller import Controller
from asim.utils import scale


def main(args, controller):
    game = gym.make(args.gamename)
    obs = game.reset()
    action_names = game.get_action_meanings()
    action_keys = []

    print('All action names: {}'.format(action_names))
    print('Start recording...')
    
    img = scale(obs, 600, 800)
    controller.update_title(args.gamename)
    controller.update(img)

    for i in range(len(action_names)):
        name = action_names[i]
        print('{}-th action, name={}, waiting...'.format(i, name))
        action = controller.get_last_key()
        action_keys.append(action)
        print('{}-th action, name={}, key={}, done.'.format(i, name, repr(action)))
    print('Recording end.')

    print('Recoding quit action key')
    quit_key = controller.get_last_key() 
    print('quit action, key={}, done.'.format(repr(quit_key)))

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

    controller = Controller()
    thread = threading.Thread(target=main, args=(parser.parse_args(), controller))

    thread.start()
    controller.mainloop()
   
