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


reload(sys)
sys.setdefaultencoding("utf-8")

LOG_FILE_NAME = 'log.log'
GROUP_FOLLOW_FILENAME = 'groupfollow.txt'
CLIENT_ID = 53999199
VPATH = './v_%s.png'

WEB_QQ_URL = 'http://w.qq.com/'
UI_PTLOGIN2_URL = 'https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001'


BUDDY_URL = 'http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq={0}&clientid={1}&psessionid={2}&t={3}'

REFERER_URL = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
# Referer = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
HTTPS_REFERER_URL = 'https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1'



QQ_LOGIN_URL = 'https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken={0}&webqq_type=10&remember_uin=1&login2qq=1&aid={1}&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-{2}&mibao_css={3}&t=1&g=1&js_type=0&js_ver={4}&login_sig={5}&pt_randsalt=2'

LOGINED_CHECK_URL = 'http://d1.web2.qq.com/channel/login2'
LOGINED_CHECK_REFER_URL = 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2'

# LOGINED_CHECK_VERIFY_URL = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq={0}&clientid={1}&psessionid={2}&t={3}"
LOGINED_CHECK_VERIFY_URL = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq={0}&clientid={1}&psessionid={2}&t={3}"

QQ_GROUP_API_URL = 'http://s.web2.qq.com/api/get_group_name_list_mask2'

VRCODE_DOWNLOAD_URL = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid={0}&e=0&l=M&s=5&d=72&v=4&t=0.0836106{1}4250{2}6653'

CHECK_MSG_URL = 'https://d1.web2.qq.com/channel/poll2'

SEND_SESS_MSG_URL = "https://d1.web2.qq.com/channel/send_sess_msg2"

SEND_BUDDY_MSG_URL = "https://d1.web2.qq.com/channel/send_buddy_msg2"
GET_GROUP_INFO_URL = 'http://s.web2.qq.com/api/get_group_info_ext2?gcode={0}&vfwebqq={1}&t={2}'

TULING_API_URL = 'http://www.tuling123.com/openapi/api?'
TULING_KEY= '4fbe28a1ace8412b997a01498d7b2513'

logging.basicConfig(filename=LOG_FILE_NAME, level=logging.DEBUG, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')