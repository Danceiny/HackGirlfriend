# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
# from PackageNormalData import *
from flask import Blueprint, request, jsonify, redirect, template_rendered,g,render_template,send_from_directory,url_for,current_app
import requests
import urllib
import os
import urllib2
import os
import time
from contextlib import contextmanager
import threading
import multiprocessing
import threadpool

from Libraries.Utils import *
from Libraries.ErrorDefine import *

# 实例化一个blueprint
QQBot = Blueprint("QQBot", __name__,template_folder='templates',static_folder='static',static_url_path='qqbot/static')
from Libraries.mythreadpool import *
from Platform.QQBotCenter.QQBotCenter import QQBotCenter
qqBotCenter = QQBotCenter.instance()
from flask import current_app

@QQBot.route('qqbot/one',methods=['GET'],endpoint='oneclickstart')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def oneclickstart():
    data = request.data
    groups = []
    if data != None and any(data):
        values = data.get('v')
        if isinstance(values,(unicode,str)):
            values = values.encode('utf-8')
        for v in values.split(','):
            groups.append(v.decode('utf8','ignore'))
    print 'groups',groups

    kwargs = qqBotCenter.getQRUrlDelegate()

    # qqBotCenter.continueLogin(groups,kwargs)
    if data.get('use_celery','true') != 'true':
        t = threading.Thread(target=qqBotCenter.loginWithDelegate, args=groups,
                             kwargs=kwargs)
        t.setDaemon(True)
        t.start()  # 不能join，join就堵塞了，无法返回
    else:
        qqBotCenter.loginWithDelegate()

    lazy_js_path = url_for('static',filename='js/lazysizes.min.js')
    min_img = url_for('QQBot.static',filename='images/qrcode-min.png')
    img = url_for('QQBot.static',filename='/'.join(('images', os.path.basename(kwargs.get('url')))))


    return render_template('QRCode.html',lazy_js_path=lazy_js_path,static_img=min_img,img=img,watch_group=groups),200,{"Cache-Control": "no-cache, no-store, must-revalidate"}
    # return redirect(vpath_url)

@QQBot.route('qqbot/set',methods=['GET'],endpoint='qqbot_set')
@check_api_cost_time
@allow_cross_domain
def qqbot_set():

    return render_template('index.html')