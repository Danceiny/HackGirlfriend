#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from Libraries.Singleton.Singleton import Singleton
from Libraries.MyLogger import MyLogger

@Singleton
class LogCenter(object):
    def __init__(self):
        self.logger_map = {}

    def get_logger(self, name):
        """ return logger"""
        if not self.logger_map.has_key(name):
            self.logger_map[name] = MyLogger(name)
        return self.logger_map[name]