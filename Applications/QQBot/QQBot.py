# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
# from PackageNormalData import *
from flask import Blueprint, request, jsonify, redirect, template_rendered,g,render_template,send_from_directory,url_for
import requests
import urllib
import os
from contextlib import contextmanager
from Libraries.Utils import *
from Libraries.ErrorDefine import *

# 实例化一个blueprint
QQBot = Blueprint("QQBot", __name__)

from Platform.QQBotCenter.QQBotCenter import QQBotCenter

qqBotCenter = QQBotCenter.instance()

import threading
import thread
@QQBot.route('qqbot/oneclickstart',methods=['GET'],endpoint='oneclickstart')
@check_api_cost_time
# @package_json_request_data
@allow_cross_domain
def oneclickstart():
    result = {'code':ED.no_err}
    # data = request.data
    # template = url_for('qrcode','/Applications/static/templates/QRCode.html')
    # thread.start_new_thread(qqBotCenter.oneclickstart,())
    # return send_from_directory('Applications/QQBot/templates','QRCode.html')
    vpath = os.path.abspath('Applications/static/images/qrcode.png')
    print vpath
    vpath = 'Applications/static/images/qrcode.png'
    vpath = url_for('static',filename='images/qrcode.png')
    return render_template('QRCode.html',img_qrcode=vpath)

@QQBot.route('qqbot/login',methods = ['GET'],endpoint='loginPage')
@check_api_cost_time
def loginPage():
    pass
    # return 'hello world'

