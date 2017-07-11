#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from Libraries.Singleton.Singleton import Singleton

#from SecretDBManager import SecretDBManager
from Platform.LogCenter.LogCenter import LogCenter


@Singleton
class SecretCenter(object):
    def __init__(self):
        self.logger = LogCenter.instance().get_logger('SecretCenterLog')
        #self.newsDBManager = SecretDBManager.instance()

    def get_user_info(self,data):
        pass

