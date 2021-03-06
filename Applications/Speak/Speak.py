# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
from flask import Blueprint, request, jsonify, redirect, render_template
import requests
import urllib
from Libraries.Utils import *
import PackageData.BaiduYuyin as baidu
from Platform.ChatbotCenter.ChatbotCenter import ChatbotCenter
from Platform.SpeakCenter.SpeakCenter import SpeakCenter

# 实例化一个blueprint
Speak = Blueprint("Speak", __name__)
chatbotCenter = ChatbotCenter()
speakCenter = SpeakCenter()

@check_api_cost_time
@allow_cross_domain
@package_json_request_data
@Speak.route('v1/speak/chatbot',methods = ['POST','GET'],endpoint='chatbot_reply')
def chatbot_reply():
    result = {'code':ED.no_err,'data':{}}
    data = request.data
    # data = {mode:'',sent:'',password:'',email:'',role:'',...}
    if data != None:
        if data.get('mode') == 'simple':
            result = chatbotCenter.simple_reply(data)
        elif data.get('mode') == 'complicate':
            result = chatbotCenter.complicate_reply(data)
        else:
            result['code'] = ED.err_params
    else:
        result['code'] = ED.err_sys
    return json.dumps(result)

@Speak.route('speak/<string:words>')
def speak_words(words):
    # return 'speak'
    # words must less then 1024 bytes
    DEFAULT_LAN = 'zh'
    DEFAULT_CTP = 1  # client type, 1 as web
    DEFAULT_SPEED = 5  # like baidu
    DEFAULT_PER = 0  # like baidu, woman
    DEFAULT_PIT = 5  # 音调
    DEFAULT_VOL = 5  # 音调
    strSize = sys.getsizeof(words)
    if strSize > 1024:
        print 'The text words must be less than 1024 bytes'
        return -1
    tex = words
    lan = DEFAULT_LAN
    tok = baidu.ACCESS_TOKEN
    ctp = DEFAULT_CTP
    cuid = get_mac_address()
    spd = DEFAULT_SPEED
    per = DEFAULT_PER
    vol = DEFAULT_VOL
    pit = DEFAULT_PIT
    return request_api(tex,lan,tok,ctp,cuid,spd,pit,vol,per)



def request_api(tex,lan,tok,ctp,cuid,spd,pit,vol,per):
    url = baidu.API_BASE_URL + '?tex=%s&lan=%s&tok=%s&ctp=%d&cuid=%s&spd=%d&pit=%d&vol=%d&per=%d' % (tex,lan,tok,ctp,cuid,spd,pit,vol,per)
    # response = requests.get(url, stream=True)
    voice_data = urllib.urlopen(url).read()

    cur_file_path = os.getcwd()
    if not cur_file_path.endswith('Applications'):
        cur_file_path = concat_dirs(True, cur_file_path, 'Applications')
    abs_vpath = concat_dirs(True, cur_file_path, 'QQBot', 'static', 'images',
                            'voice_{}.mp3'.format(get_now_time_str_ms().replace('.', '')))

    print abs_vpath,'abs_va'
    voice_fp = open(abs_vpath,'wb+')
    voice_fp.write(voice_data)
    voice_fp.close()
    return 'write success'
