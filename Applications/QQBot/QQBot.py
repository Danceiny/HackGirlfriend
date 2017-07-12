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
QQBot = Blueprint("QQBot", __name__,template_folder='templates',static_folder='static',static_url_path='qqbot/static')

from Platform.QQBotCenter.QQBotCenter import QQBotCenter,oneclickstart

qqBotCenter = QQBotCenter.instance()
import threading
from Libraries.mythreadpool import *

@QQBot.route('qqbot/one',methods=['GET'],endpoint='oneclickstart')
@check_api_cost_time
@allow_cross_domain
def oneclickstart():
    if request.method == "POST":
        request.data = json.loads(request.data)
    else:
        temp_raw_data = request.args.items()
        print 'temp_raw_data',temp_raw_data
        temp_raw_map = {}
        for temp_item in temp_raw_data:
            # print('type',type(temp_item),type(temp_raw_data[temp_item]))
            temp_raw_map[temp_item[0]] = temp_item[1]
        request.data = temp_raw_map
    data = request.data
    groups = []
    if data != None:
        values = data.get('v')
        if isinstance(values,unicode):
            values = values.encode('utf-8')
        for v in values.split(','):
            print 'get params',v
            groups.append(v.decode('utf8','ignore'))
    print 'groups',groups

    wm = WorkerManager(2) # 创建线程池
    wm.add_job(qqBotCenter.getQRCodeUrl) # 将所有请求加入队列中
    wm.start()
    wm.wait_for_complete()
    kwargs = wm.get_result()
    kwargs['groups'] = groups


    # thread.start_new_thread(qqBotCenter.continueLogin,(kwargs,))
    # t = threading.Thread(target=qqBotCenter.continueLogin, args=(kwargs,))
    # t.setDaemon(True)
    # t.start()#不能join，join就堵塞了，无法返回

    # 多进程： windows上开不起来？？？
    # p = multiprocessing.Process(target=oneclickstart, args=())
    # p.start()
    # p.join()
    lazy_js_path = url_for('static',filename='js/lazysizes.min.js')
    min_img = url_for('QQBot.static',filename='images/qrcode-min.png')
    img = url_for('QQBot.static',filename='/'.join(('images/' + os.path.basename(wm.get_result().get('url')))))

    wm.add_job(qqBotCenter.continueLogin,(kwargs,))
    wm.start()
    return render_template('QRCode.html',lazy_js_path=lazy_js_path,static_img=min_img,img=img),200,{"Cache-Control": "no-cache, no-store, must-revalidate"}
    # return redirect(vpath_url)

@QQBot.route('qqbot/set',methods=['GET'],endpoint='qqbot_set')
@check_api_cost_time
@allow_cross_domain
def qqbot_set():

    return render_template('index.html')