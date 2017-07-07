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
import Util as util

from QMessage import QMessage
from Login import Login
from CONFIGS import *

from Libraries.Singleton import Singleton
reload(sys)
sys.setdefaultencoding("utf-8")


@Singleton


@Singleton
class ConfigCenter(object):

    initTime = time.time()
    HttpClient_Ist = HttpClient()
    own_qq_number = 0

    try:
        initTime,_ = util.pass_time(initTime)

        params = {'PSessionID':''}
        qqLogin = Login(own_qq_number,params)
        qqLogin.login()

    except Exception, e:
        logging.critical(str(e))
        os._exit(1)


    t_check = QMessage(HttpClient_Ist,qqLogin)


    t_check.setDaemon(True)
    t_check.start()
    t_check.watch_group(t_check.GroupNameList, t_check.GroupCodeList)

    try:
        with open(GROUP_FOLLOW_FILENAME,'r') as f:
            for line in f:
                tmp = line.strip('\n').strip('\r')
                if str(tmp) in t_check.GroupNameList:
                    t_check.GroupWatchList.append(str(t_check.GroupNameList[str(tmp)]))
                    logging.info("关注:"+str(tmp))
                else:
                    logging.error("无法找到群：" + str(tmp))
    except Exception, e:
        logging.error("读取组存档出错:"+str(e))



    t_check.join()
