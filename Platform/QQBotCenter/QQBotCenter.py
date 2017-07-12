# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from CONFIGS import *

from Libraries.Singleton.Singleton import Singleton
import QQBot
from HttpClient import HttpClient


def oneclickstart():
    # 只有top module的函数才能序列化（多进程调用的target）
    QQBot.main(mode='api')

@Singleton
class QQBotCenter(object):


    def __init__(self):
        pass

    def oneclickstart(self,groups):
        print('QQBotcenter.py onclickstart',groups)
        QQBot.main(mode='api',groups=groups)


    def getQRCodeUrl(self):
        return QQBot.getQRCodeUrl()

    def continueLogin(self,kwargs):
        QQBot.loginWithDelegate(qqLoginDelegate=kwargs.get('delegate',None),params=kwargs.get('params',None),HttpClient_Ist=kwargs.get('httpclient',HttpClient()))