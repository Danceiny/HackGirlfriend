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
from CONFIGS import *

reload(sys)
sys.setdefaultencoding("utf-8")


def getReValue(html, rex, er, ex):
    v = re.search(rex, html)

    if v is None:
        logging.error(er)
        print 'error %s' % er
        if ex:
            raise Exception, er
        return ''

    return v.group(1)


class Login(HttpClient):
    def __init__(self, qq_number=0, params=None):
        print 'class Login init....'
        self.initTime = time.time()
        # self.VPath = VPATH % util.convert_int_2_string_single(int(time.time()))  # QRCode保存路径
        self.VPath = params.get('VPATH',VPATH % str(int(time.time()))) # QRCode保存路径
        self.PSessionID = params.get('PSessionID', '')
        self.MaxTryTime = params.get('MaxTryTime', 5)
        self.DELETE_PIC = params.get('DELETE_PIC',True)
        self.QR_AVALABLE = False
        self.AdminQQ = int(qq_number)
        self.preLogined = False

    def getQRCode(self,Try=0):
        if self.preLogined:
            self.Download((VRCODE_DOWNLOAD_URL).format(self.APPID, random.randint(0, 9), random.randint(0, 9)),self.VPath)
            logging.info('[{0}] Get QRCode Picture Success.'.format(Try))
            self.QRSig = self.getCookie('qrsig')
            logging.info('get QRSig : %s', self.QRSig)
        else:
            self.preLogin()

    def checkQRCode(self,Try=0,StartTime=None):
        if StartTime == None:StartTime = util.date_to_millis(datetime.datetime.utcnow())
        while True:
            Try += 1
            login_html = self.Get((QQ_LOGIN_URL).format(util.getQRtoken(self.QRSig), self.APPID,
                                                        util.date_to_millis(datetime.datetime.utcnow()) - StartTime,
                                                        self.MiBaoCss, self.JS_VERSION, self.SIGN),UI_PTLOGIN2_URL)
            logging.info('[{0}] Get QQ_LOGIN_URL html, %s'.format(Try),login_html)
            ret = login_html.split("'")
            logging.info(ret)

            if ret[1] == '66':
                if os.path.exists(self.VPath):
                    self.QR_AVALABLE = True
                    break
                else:
                    self.getQRCode(Try)
                    continue
            elif ret[1] == '65':
                if os.path.exists(self.VPath) and self.DELETE_PIC:
                    os.remove(self.VPath)
                    self.getQRCode()
                continue
            elif ret[1] == '0':  # 65: QRCode 失效, 0: 验证成功, 66: 未失效, 67: 验证中
                self.QR_AVALABLE = False
                # 删除QRCode文件
                if os.path.exists(self.VPath) and self.DELETE_PIC:
                    os.remove(self.VPath)
                break
            time.sleep(5)
        logging.info('跳出登陆的True死循环')
        return ret

    def preLogin(self):
        # 1. 获取登录页面
        logging.critical("正在获取登陆页面")
        self.Get(WEB_QQ_URL)
        login_html = self.Get(UI_PTLOGIN2_URL, WEB_QQ_URL)
        logging.info('get login_html : %s', login_html)

        # 2. 获取appid
        logging.critical("正在获取appid")
        self.APPID = getReValue(login_html, r'<input type="hidden" name="aid" value="(\d+)" />', 'Get AppId Error', 1)
        logging.info('get appid : %s', self.APPID)

        # 3. 获取登录证书 sign
        logging.critical("正在获取login_sig")
        self.SIGN = getReValue(login_html, r'g_login_sig\s*=\s*encodeURIComponent\s*\("(.*?)"\)',
                               'Get Login Sign Error', 0)

        logging.info('get sign : %s', self.SIGN)

        # 4. 获取js版本
        logging.critical("正在获取pt_version")
        self.JS_VERSION = getReValue(login_html, r'g_pt_version\s*=\s*encodeURIComponent\s*\("(\d+)"\)',
                                     'Get g_pt_version Error', 1)

        logging.info('get g_pt_version : %s', self.JS_VERSION)

        # 5. 获取css
        logging.critical("正在获取mibao_css")

        self.MiBaoCss = getReValue(login_html, r'g_mibao_css\s*=\s*encodeURIComponent\s*\("(.*?)"\)',
                                   'Get g_mibao_css Error', 1)
        logging.info('get g_mibao_css : %s', self.MiBaoCss)

        self.preLogined = True


    def scanQR(self):
        # 6. 扫码
        StartTime = util.date_to_millis(datetime.datetime.utcnow())


        if not self.QR_AVALABLE:
            logging.info('QR is not avalable, to download it...')
            self.getQRCode()


        ret = self.checkQRCode(StartTime)
        logging.critical('Finish Check QR code...')
        if ret[1] != '0':
            raise ValueError, "RetCode = " + ret['retcode']
            return
        logging.critical("二维码已扫描，正在登陆")

        self.initTime, _ = util.pass_time(self.initTime)
        # 删除QRCode文件
        if os.path.exists(self.VPath) and self.DELETE_PIC:
            os.remove(self.VPath)
        return ret


    def login(self):
        if not self.preLogined: self.preLogin()

        ret = self.scanQR()

        # 记录登陆账号的昵称
        self.tmpUserName = ret[11]
        logging.info('登录账号的昵称是：%s' % self.tmpUserName)

        # ????
        login_html = self.Get(ret[5],REFERER_URL)
        logging.info('Get ret[5] html: %s',login_html)
        # proxy_iframe.src = "http://web2.qq.com/web2_cookie_proxy.html";
        url = getReValue(login_html, r' src="(.+?)"', 'Get mibao_res Url Error.', 0)
        if url != '':
            login_html = self.Get(url.replace('&amp;', '&'))
            url = getReValue(login_html, r'location\.href="(.+?)"', 'Get Redirect Url Error', 1)
            login_html = self.Get(url)

        self.PTWebQQ = self.getCookie('ptwebqq')
        logging.info('PTWebQQ: {0}'.format(self.PTWebQQ))

        LoginError = 3
        while LoginError > 0:
            try:
                #沒有 下面的html2，就無法找到群
                # html2 = self.Get(
                #     "http://s.web2.qq.com/api/getvfwebqq?ptwebqq={0}&clientid={1}&psessionid={2}&t={3}".format(PTWebQQ,
                #                                                                                                ClientID,
                #                                                                                                PSessionID,
                #                                                                                                get_ts()),
                #     Referer)
                reqUrl = (LOGINED_CHECK_VERIFY_URL).format(self.PTWebQQ, CLIENT_ID, self.PSessionID, util.get_ts())
                # reqUrl = (LOGINED_CHECK_VERIFY_URL).format(self.PTWebQQ, CLIENT_ID, self.PSessionID, int(time.time()))
                # reqUrl = (LOGINED_CHECK_VERIFY_URL).format(self.PTWebQQ, CLIENT_ID,int(time.time()))

                logging.info('get找到群的url: %s',reqUrl)
                html2 = self.Get(reqUrl,REFERER_URL)
                logging.info("[{0}] getvfwebqq html: %s".format(3-LoginError),str(html2))
                ret2 = json.loads(html2)
                # self.PSessionID = ret2['result']['psessionid']
                # self.VFWebQQ = ret2['result']['vfwebqq']

                login_html = self.Post(LOGINED_CHECK_URL, {
                    'r': '{{"ptwebqq":"{0}","clientid":{1},"psessionid":"{2}","status":"online"}}'.format(self.PTWebQQ,
                                                                                                          CLIENT_ID,
                                                                                                          self.PSessionID)
                }, LOGINED_CHECK_REFER_URL)
                logging.info('[{0}] check login_html: %s'.format(3-LoginError),login_html)
                # login_html = {"result": {"cip": 23600812, "f": 0, "index": 1075, "port": 47450,
                #             "psessionid": "8368046764001d636f6e6e7365727665725f77656271714031302e3133332e34312e383400001ad00000066b026e040015808a206d0000000a406172314338344a69526d0000002859185d94e66218548d1ecb1a12513c86126b3afb97a3c2955b1070324790733ddb059ab166de6857",
                #             "status": "online", "uin": 491976401, "user_state": 0,
                #             "vfwebqq": "59185d94e66218548d1ecb1a12513c86126b3afb97a3c2955b1070324790733ddb059ab166de6857"},
                #  "retcode": 0}
                ret = json.loads(login_html)


                LoginError = 0
            except:
                LoginError -= 1
                logging.critical("登录失败，正在重试")

        # if ret['retcode'] != 0 or ret2['retcode'] != 0:
        if ret['retcode'] != 0:
            raise ValueError, "Login Retcode=" + str(ret['retcode'])
            return

        self.VFWebQQ = ret2['result']['vfwebqq']
        self.PSessionID = ret['result']['psessionid']

        self.MyUIN = ret['result']['uin']
        logging.critical("QQ号：{0} 登陆成功, 用户名：{1}".format(ret['result']['uin'], self.tmpUserName))
        logging.info('Login success')
        logging.critical("登陆二维码用时" + util.pass_time(self.initTime)[1] + "秒")
