# -*- coding:utf8 -*-
# File   : utils.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com 
# 
# This file is part of Atari-Simulator.

import os.path as osp
import sys
import importlib

def load_module(module_name):
    module = importlib.import_module(module_name)
    return module

def load_module_filename(module_filename):
    if not module_filename.endswith('.py'):
        module_filename += '.py'

    real_path = osp.realpath(module_filename)
    dirname = osp.dirname(real_path)
    filename = osp.basename(real_path)[:-3]

    sys.path.insert(0, dirname)
    module = load_module(filename)
    del sys.path[0]

    return module


def module_vars_as_dict(module):
    res = {}
    for k in dir(module):
        if not k.startswith('__'):
            res[k] = getattr(module, k)
    return res


def scale(img, min_dim, max_dim):
    import cv2

    h, w = img.shape[:2]
    if h > w:
        s = min(max_dim / h, min_dim / w)
    else:
        s = max(max_dim / w, min_dim / h)
    hh, ww = int(h*s), int(w*s)
    return cv2.resize(img, (ww, hh))


