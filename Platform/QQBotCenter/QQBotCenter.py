# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from CONFIGS import *

from Libraries.Singleton.Singleton import Singleton


@Singleton
class QQBotCenter(object):
    def __init__(self):
        pass

    def oneclickstart(self):
        import QQBot
        QQBot.main()
