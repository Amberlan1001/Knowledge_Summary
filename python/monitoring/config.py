#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author       : zch
@CreateTime   : 2020-06-30 20:23:26
@LastEditTime : 2020-10-14 17:22:16
@FilePath     : /monitoring/config.py
@Description  : 
'''
import os
import yaml
import threading

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

conf_default_path = os.path.dirname(os.path.dirname(__file__)) + '/monitor.yaml'

class Config(object):
    singleton = None
    mutex = threading.Lock()

    @staticmethod
    def get_instance():
        if Config.singleton is None:
            Config.mutex.acquire()
            if Config.singleton is None:
                Config.singleton = Config()
            Config.mutex.release()
        return Config.singleton

    def __init__(self, config_path=conf_default_path):
        with open(config_path, encoding='utf8') as config_file:
            self.conf = yaml.load(config_file, Loader=Loader)

monitor = Config.get_instance().conf['monitor']

