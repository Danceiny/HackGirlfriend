# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
# from PackageNormalData import *
from flask import Blueprint, request, jsonify, redirect, render_template
import requests
import urllib

import Libraries.Utils as utils
import PackageData.BaiduYuyin as baidu

# 实例化一个blueprint
Speak = Blueprint("Speak", __name__)

# @Speak.route('/')
# def root():
#     return 'Hello World!'


DEFAULT_LAN = 'zh'
DEFAULT_CTP = 1 # client type, 1 as web
DEFAULT_SPEED = 5   # like baidu
DEFAULT_PER = 0 # like baidu, woman
DEFAULT_PIT = 5 # 音调
DEFAULT_VOL = 5 # 音调


@Speak.route('speak/<string:words>')
def speak_words(words):
    # return 'speak'
    # words must less then 1024 bytes
    strSize = sys.getsizeof(words)
    if strSize > 1024:
        print 'The text words must be less than 1024 bytes'
        return -1
    tex = words
    lan = DEFAULT_LAN
    tok = baidu.ACCESS_TOKEN
    ctp = DEFAULT_CTP
    cuid = utils.get_mac_address()
    spd = DEFAULT_SPEED
    per = DEFAULT_PER
    vol = DEFAULT_VOL
    pit = DEFAULT_PIT
    return request_api(tex,lan,tok,ctp,cuid,spd,pit,vol,per)



def request_api(tex,lan,tok,ctp,cuid,spd,pit,vol,per):
    url = baidu.API_BASE_URL + '?tex=%s&lan=%s&tok=%s&ctp=%d&cuid=%s&spd=%d&pit=%d&vol=%d&per=%d' % (tex,lan,tok,ctp,cuid,spd,pit,vol,per)
    # response = requests.get(url, stream=True)
    voice_data = urllib.urlopen(url).read()

    voice_fp = open('voice.mp3','wb+')
    voice_fp.write(voice_data)
    voice_fp.close()
    return 'write success'
