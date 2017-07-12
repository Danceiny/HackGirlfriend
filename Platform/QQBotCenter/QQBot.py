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
import traceback
from HttpClient import HttpClient
import Utils as util
from Libraries.Utils import concat_dirs
from QMessage import QMessage
from Login import Login
from CONFIGS import *

def getQRCodeUrl(own_qq_number=0):
    HttpClient_Ist = HttpClient()
    try:
        cur_file_path = os.getcwd()
        print 'cur_file_path',cur_file_path
        vpath = concat_dirs(cur_file_path, 'static', 'images','qrcode.png')
        print('vpath',vpath)
        params = {'DELETE_PIC': True, 'VPATH': VPATH if vpath == '' else vpath}
        qqLoginDelegate = Login(own_qq_number, params)
        qqLoginDelegate.preLogin()
        url = qqLoginDelegate.getQRCodeUrl(Try=5)
        print('qqbotcenter qqbot getqrcodeurl url',url)
        return {'delegate':qqLoginDelegate,'params':params,'url':url,'httpclient':HttpClient_Ist}
    except Exception, e:
        logging.critical(str(e))
        traceback.print_exc()
        os._exit(-11)

def main(mode='local',**kwargs):
    qqLoginDelegate = kwargs.get('delegate',None)
    initTime = time.time()
    HttpClient_Ist = HttpClient()
    if mode == 'api':
        # api mode
        ret = getQRCodeUrl()
        loginWithDelegate(qqLoginDelegate=ret.get('delegate',None),HttpClient_Ist=HttpClient_Ist,params=ret.get('params',None))
    else:
        # local mode
        try:
            initTime,_ = util.pass_time(initTime)
            cur_file_path = os.getcwd()
            vpath = ''
            if __name__ != '__main__':
                home_dir = os.path.dirname(os.path.dirname(os.path.dirname(cur_file_path)))
                vpath = os.path.join(os.path.join(os.path.join(os.path.join(home_dir,'Applications'),'static'),'images'),'qrcode.png')
            params = {'DELETE_PIC':True,'VPATH':VPATH if vpath == '' else vpath}
            qqLoginDelegate = Login(0,params)
            qqLoginDelegate.login()
            loginWithDelegate(qqLoginDelegate,HttpClient_Ist,params)
        except Exception, e:
            logging.critical(str(e))
            os._exit(1)

def loginWithDelegate(qqLoginDelegate=None,HttpClient_Ist=None,params=None):
    if qqLoginDelegate != None:
        qqLoginDelegate.login()
        t_check = QMessage(HttpClient_Ist,qqLoginDelegate,params=params)

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