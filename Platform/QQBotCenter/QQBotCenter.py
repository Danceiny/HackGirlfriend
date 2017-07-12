# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from CONFIGS import *

from Libraries.Singleton.Singleton import Singleton
import QQBot
from HttpClient import HttpClient
@Singleton
class QQBotCenter(object):


    def __init__(self):
        pass

    def oneclickstart(self):
        QQBot.main(mode='api')

    def getQRCodeUrl(self):
        return QQBot.getQRCodeUrl()

    def continueLogin(self,kwargs):
        QQBot.loginWithDelegate(qqLoginDelegate=kwargs.get('delegate',None),params=kwargs.get('params',None),HttpClient_Ist=kwargs.get('httpclient',HttpClient()))