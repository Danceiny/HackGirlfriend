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

def getQRCodeUrl(own_qq_number=0,HttpClient_Ist=None):
    try:
        cur_file_path = os.getcwd()
        if not cur_file_path.endswith('Applications'):
            cur_file_path = concat_dirs(cur_file_path,'Applications')
        vpath = concat_dirs(cur_file_path,'QQBot','static', 'images','qrcode.png')
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
    print('QQBotcenter.py onclickstart', kwargs.get('groups',[]))
    initTime = time.time()
    HttpClient_Ist = HttpClient()
    if mode == 'api':
        # api mode
        ret = getQRCodeUrl(HttpClient_Ist=HttpClient_Ist)
        loginWithDelegate(qqLoginDelegate=ret.get('delegate',None),HttpClient_Ist=HttpClient_Ist,params=ret.get('params',None),groups=kwargs.get('groups',[]))
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

def loginWithDelegate(qqLoginDelegate=None,HttpClient_Ist=None,params=None,groups=None):
    if qqLoginDelegate != None:
        qqLoginDelegate.login()
        t_check = QMessage(HttpClient_Ist,qqLoginDelegate,params=params)

        t_check.setDaemon(True)
        t_check.start()

        # 把所有群加进t_check实例的GroupNameList，GroupCodeList列表中
        t_check.watch_group()

        try:
            for group in groups:
                tmp = group.strip('\n').strip('\r').strip()
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