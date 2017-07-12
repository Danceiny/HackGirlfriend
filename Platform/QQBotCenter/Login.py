# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import random
import json
import os

import datetime
import time
from HttpClient import HttpClient
import Utils as util
from CONFIGS import *


def getReValue(html, rex, er, ex):
    v = re.search(rex, html)

    if v is None:
        logger.error(er)
        print 'error %s' % er
        if ex:
            raise Exception, er
        return ''

    return v.group(1)


class Login(HttpClient):
    def __init__(self, qq_number=0, params=None):
        self.initTime = time.time()
        self.VPath = params.get('VPATH',VPATH % str(int(time.time()))) # QRCode保存路径
        self.PSessionID = params.get('PSessionID', '')
        self.MaxTryTime = params.get('MaxTryTime', 5)
        self.DELETE_PIC = params.get('DELETE_PIC',True)
        self.QR_AVALABLE = False
        self.AdminQQ = int(qq_number)
        self.preLogined = False

    def getQRCodeUrl(self,Try=0):
        logger.info('[{0}] Get QRCode Picture Success.'.format(Try))
        url = VRCODE_DOWNLOAD_URL.format(self.APPID, random.randint(0, 9), random.randint(0, 9))
        self.Download(url,self.VPath)
        self.QRSig = self.getCookie('qrsig')
        print 'getQRCodeUrl',self.QRSig
        logger.info('get QRSig : %s'% self.QRSig)
        self.QR_AVALABLE = True
        return self.VPath

    def downloadQRCode(self, Try=0):
        if self.preLogined:
            self.Download((VRCODE_DOWNLOAD_URL).format(self.APPID, random.randint(0, 9), random.randint(0, 9)),self.VPath)
            logger.info('[{0}] Get QRCode Picture Success.'.format(Try))
            self.QRSig = self.getCookie('qrsig')
            logger.info('get QRSig : %s'%self.QRSig)
            self.QR_AVALABLE = True
        else:
            self.preLogin()

    def checkQRCode(self,Try=0,StartTime=None):
        if StartTime == None:StartTime = util.date_to_millis(datetime.datetime.utcnow())
        ret = None
        while True:
            Try += 1
            if not self.QR_AVALABLE:
                self.getQRCodeUrl(Try=Try)
            while True:
                url = (QQ_LOGIN_URL).format(util.getQRtoken(self.QRSig), self.APPID,
                                            util.date_to_millis(datetime.datetime.utcnow()) - StartTime,
                                            self.MiBaoCss, self.JS_VERSION, self.SIGN)
                login_html = self.Get(url, UI_PTLOGIN2_URL)
                logger.info('[{0}] Get QQ_LOGIN_URL html, %s'.format(Try))
                ret = login_html.split("'")
                logger.info('checkQRCode retvalue %d '% len(ret))
                if len(ret) < 2:
                    time.sleep(2)
                    continue
                if ret[1] == '0':  # 65: QRCode 失效, 0: 验证成功, 66: 未失效, 67: 验证中
                    self.QR_AVALABLE = False
                    # 删除QRCode文件
                    if os.path.exists(self.VPath) and self.DELETE_PIC:
                        os.remove(self.VPath)
                    break
                elif ret[1] == '65':
                    self.QR_AVALABLE = False
                    if os.path.exists(self.VPath) and self.DELETE_PIC:
                        os.remove(self.VPath)
                    time.sleep(2)
                    self.downloadQRCode()
                    continue

                elif ret[1] == '67':
                    time.sleep(2)
                    continue
                time.sleep(2)
            if ret[1] == '0' or Try > self.MaxTryTime:
                break
        logger.info('跳出登陆的True死循环')
        return ret

    def scanQR(self):
        # 6. 扫码
        StartTime = util.date_to_millis(datetime.datetime.utcnow())
        if not self.QR_AVALABLE:
            logger.info('QR is not avalable, to download it...')
            self.downloadQRCode()
        ret = self.checkQRCode(StartTime)

        logger.critical('Finish Check QR code...')
        if ret[1] != '0':
            raise ValueError, "RetCode = " + ret['retcode']
            return
        logger.critical("二维码已扫描，正在登陆")

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
        logger.info('登录账号的昵称是：%s' % self.tmpUserName)
        login_html = self.Get(ret[5],REFERER_URL)
        logger.info('Get ret[5] html: %s',login_html)
        # proxy_iframe.src = "http://web2.qq.com/web2_cookie_proxy.html";
        url = getReValue(login_html, r' src="(.+?)"', 'Get mibao_res Url Error.', 0)
        if url != '':
            login_html = self.Get(url.replace('&amp;', '&'))
            url = getReValue(login_html, r'location\.href="(.+?)"', 'Get Redirect Url Error', 1)
            login_html = self.Get(url)
        self.PTWebQQ = self.getCookie('ptwebqq')
        logger.info('PTWebQQ: {0}'.format(self.PTWebQQ))
        LoginError = 3
        ret2 = None
        while LoginError > 0:
            try:
                reqUrl = (LOGINED_CHECK_VERIFY_URL).format(self.PTWebQQ, CLIENT_ID, self.PSessionID, util.get_ts())

                logger.info('get找到群的url: %s',reqUrl)
                html2 = self.Get(reqUrl,REFERER_URL)
                logger.info("[{0}] getvfwebqq html: %s".format(3-LoginError),str(html2))
                ret2 = json.loads(html2)
                login_html = self.Post(LOGINED_CHECK_URL, {
                    'r': '{{"ptwebqq":"{0}","clientid":{1},"psessionid":"{2}","status":"online"}}'.format(self.PTWebQQ,
                                                                                                          CLIENT_ID,
                                                                                                          self.PSessionID)
                }, LOGINED_CHECK_REFER_URL)
                logger.info('[{0}] check login_html: %s'.format(3-LoginError),login_html)
                ret = json.loads(login_html)
                LoginError = 0
            except:
                LoginError -= 1
                logger.critical("登录失败，正在重试")
        if ret['retcode'] != 0:
            raise ValueError, "Login Retcode=" + str(ret['retcode'])
            return

        self.VFWebQQ = ret2['result']['vfwebqq']
        self.PSessionID = ret['result']['psessionid']

        self.MyUIN = ret['result']['uin']
        logger.info("QQ号：{0} 登陆成功, 用户名：{1}".format(ret['result']['uin'], self.tmpUserName))
        logger.info('Login success')
        logger.info("登陆二维码用时" + util.pass_time(self.initTime)[1] + "秒")

    def preLogin(self):
        # 1. 获取登录页面
        logger.info("正在获取登陆页面")
        self.Get(WEB_QQ_URL)
        login_html = self.Get(UI_PTLOGIN2_URL, WEB_QQ_URL)
        # 2. 获取appid
        logger.info("正在获取appid")
        self.APPID = getReValue(login_html, r'<input type="hidden" name="aid" value="(\d+)" />', 'Get AppId Error', 1)
        logger.info('get appid : %s'% self.APPID)
        # 3. 获取登录证书 sign
        logger.info("正在获取login_sig")
        self.SIGN = getReValue(login_html, r'g_login_sig\s*=\s*encodeURIComponent\s*\("(.*?)"\)',
                               'Get Login Sign Error', 0)
        logger.info('get sign : %s'% self.SIGN)
        # 4. 获取js版本
        logger.info("正在获取pt_version")
        self.JS_VERSION = getReValue(login_html, r'g_pt_version\s*=\s*encodeURIComponent\s*\("(\d+)"\)',
                                     'Get g_pt_version Error', 1)
        logger.info('get g_pt_version : %s' % self.JS_VERSION)
        # 5. 获取css
        logger.info("正在获取mibao_css")
        self.MiBaoCss = getReValue(login_html, r'g_mibao_css\s*=\s*encodeURIComponent\s*\("(.*?)"\)',
                                   'Get g_mibao_css Error', 1)
        logger.info('get g_mibao_css : %s' % self.MiBaoCss)
        self.preLogined = True
