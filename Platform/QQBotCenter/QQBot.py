# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os

import time

import traceback
from HttpClient import HttpClient
import Utils as util
from Libraries.Utils import concat_dirs,get_now_time_str_ms
from QMessage import QMessage
from Login import Login
from CONFIGS import *

###########   part   #####################
def deleteAllQRCode(path):
    if os.path.isfile(path) and path.endswith(('png','jpg','gif')):
        os.remove(os.path.abspath(path))
    elif os.path.isdir(path):
        for img in os.listdir(os.path.abspath(path)):
            if os.path.isfile(img) and img.endswith(('png','jpg','gif')):
                os.remove(os.path.join(path,img))
def getQRUrlDelegate(own_qq_number=0, HttpClient_Ist=None):
    # do:
    # 1. prelogin,
    # 2. download qrcode img and return and local download abs path.
    # 3. return loginDelegate(Login() class instance), url(img abs path)

    try:
        cur_file_path = os.getcwd()
        if not cur_file_path.endswith('Applications'):
            cur_file_path = concat_dirs(True,cur_file_path,'Applications')
        abs_vpath = concat_dirs(True,cur_file_path,'QQBot','static', 'images','{}.png'.format(get_now_time_str_ms().replace('.','')))
        loginParams = {'DELETE_PIC': True, 'VPATH': VPATH if abs_vpath == '' else abs_vpath}
        qqLoginDelegate = Login(own_qq_number, loginParams)
        qqLoginDelegate.preLogin()
        url = qqLoginDelegate.getQRCodeUrl(Try=5)
        return {'loginDelegate':qqLoginDelegate,'url':url,'httpclient':HttpClient_Ist}
    except Exception, e:
        logger.error(str(e))
        traceback.print_exc()
        deleteAllQRCode()
        os._exit(-1)


def loginWithDelegate(*args,**kwargs):
    qqLoginDelegate = None
    HttpClient_Ist = None
    groups = args
    for k, v in kwargs.items():
        if 'loginDelegate' == k:
            qqLoginDelegate = v
        elif 'httpClientIst' == k:
            HttpClient_Ist = v
        elif 'loginParams' == k:
            loginParams = v

    if qqLoginDelegate != None:
        qqLoginDelegate.login()
        qMsg_Ist = QMessage(HttpClient_Ist,qqLoginDelegate)

        qMsg_Ist.setDaemon(True)
        qMsg_Ist.start()

        # 把所有群加进t_check实例的GroupNameList，GroupCodeList列表中
        qMsg_Ist.watch_group()

        try:
            for group in groups:
                tmp = group.strip('\n').strip('\r').strip()
                if str(tmp) in qMsg_Ist.GroupNameList:
                    qMsg_Ist.GroupWatchList.append(str(qMsg_Ist.GroupNameList[str(tmp)]))
                    logger.info("关注:"+str(tmp))

                else:
                    logger.error("无法找到群：" + str(tmp))
        except Exception, e:
            logger.error("读取组存档出错:"+str(e))
        qMsg_Ist.join()

##################  part  #######################

def main(mode='local',*args,**kwargs):
    groups = args
    initTime = time.time()
    HttpClient_Ist = HttpClient()
    if mode == 'api':
        # api mode
        ret = getQRUrlDelegate(HttpClient_Ist=HttpClient_Ist)
        loginWithDelegate(groups,qqLoginDelegate=ret.get('loginDelegate',None),httpClientIst=HttpClient_Ist)
    else:
        # local mode
        try:
            initTime,_ = util.pass_time(initTime)
            vpath = ''
            params = {'DELETE_PIC':True,'VPATH':VPATH if vpath == '' else vpath}
            loginDelegate = Login(0,params)
            loginDelegate.login()
            loginWithDelegate(groups, qqLoginDelegate=loginDelegate, httpClientIst=HttpClient_Ist)
        except Exception, e:
            logging.critical(str(e))
            os._exit(1)

if __name__ == "__main__":
    main('local')