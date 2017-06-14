# -*- coding: utf-8 -*-

import re
import random
import json
import os
import sys
import datetime
import time
import threading
import logging
import urllib
from HttpClient import HttpClient
import Utils as util

from QMessage import QMessage
from Login import Login
from CONFIGS import *

from Libraries.Singleton.Singleton import Singleton
reload(sys)
sys.setdefaultencoding("utf-8")


@Singleton
class QQBotCenter(object):
    def __init__(self):
        self.initTime = time.time()
    def getLoginQRCode(self):
        self.HttpClient_Ist = HttpClient()
        self.own_qq_number = 0

        try:
            self.initTime,_ = util.pass_time(self.initTime)

            params = {'VPATH':'./QQBot/img/erweima.login.png','DELETE_PIC':False}
            self.qqLogin = Login(self.own_qq_number,params)
            self.qqLogin.getQRCode()
        except Exception, e:
            logging.critical(str(e))
            os._exit(1)
        return True

    def login(self):
        try:
            self.qqLogin.login()
        except Exception, e:
            logging.critical(str(e))
            os._exit(1)
        return True


    def procMsg(self):

        t_check = QMessage(self.HttpClient_Ist,self.qqLogin)


        t_check.setDaemon(True)
        t_check.start()
        t_check.watch_group(t_check.GroupNameList, t_check.GroupCodeList)

        print os.path.realpath(__file__)
        os.chdir(os.path.realpath(__file__))
        try:
            with open(GROUP_FOLLOW_FILENAME,'r') as f:
                for line in f:
                    tmp = line.strip('\n').strip('\r')
                    print '监测的群名称：',str(tmp)
                    if str(tmp) in t_check.GroupNameList:
                        t_check.GroupWatchList.append(str(t_check.GroupNameList[str(tmp)]))
                        logging.info("关注:"+str(tmp))
                    else:
                        logging.error("无法找到群：" + str(tmp))
        except Exception, e:
            logging.error("读取组存档出错:"+str(e))



        t_check.join()
