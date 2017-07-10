# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
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
import inspect
from HttpClient import HttpClient
import Utils as util

from QMessage import QMessage
from Login import Login
from CONFIGS import *

def main():
    initTime = time.time()
    HttpClient_Ist = HttpClient()
    own_qq_number = 0
    qqLogin = None
    params = {}
    try:
        initTime,_ = util.pass_time(initTime)
        cur_file_path = inspect.getfile(inspect.currentframe())
        vpath = ''
        if __name__ != '__main__':
            home_dir = os.path.dirname(os.path.dirname(os.path.dirname(cur_file_path)))
            vpath = os.path.join(os.path.join(os.path.join(os.path.join(home_dir,'Applications'),'static'),'images'),'qrcode.png')
            print vpath
        params = {'DELETE_PIC':True,'VPATH':VPATH if vpath == '' else vpath}
        qqLogin = Login(own_qq_number,params)
        qqLogin.login()

    except Exception, e:
        logging.critical(str(e))
        os._exit(1)

    if qqLogin != None:
        t_check = QMessage(HttpClient_Ist,qqLogin,params=params)


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

if __name__ == "__main__":
    main()