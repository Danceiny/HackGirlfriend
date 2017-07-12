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
from Platform.QQBotCenter.QQBotCenter import QQBotCenter,oneclickstart
qqBotCenter = QQBotCenter.instance()

@QQBot.route('qqbot/one',methods=['GET'],endpoint='oneclickstart')
@check_api_cost_time
@allow_cross_domain
def oneclickstart():
    if request.method == "POST":
        request.data = json.loads(request.data)
    else:
        temp_raw_data = request.args.items()
        temp_raw_map = {}
        for temp_item in temp_raw_data:
            temp_raw_map[temp_item[0]] = temp_item[1]
        request.data = temp_raw_map
    data = request.data
    groups = []
    if data != None:
        values = data.get('v')
        if isinstance(values,unicode):
            values = values.encode('utf-8')
        for v in values.split(','):
            groups.append(v.decode('utf8','ignore'))
    print 'groups',groups

    # wm = WorkerManager(2) # 创建线程池
    # wm.add_job(qqBotCenter.getQRCodeUrl) # 将所有请求加入队列中
    # wm.start()
    # wm.wait_for_complete()
    # kwargs = wm.get_result()

    # wm.add_job(qqBotCenter.continueLogin,groups,kwargs)
    # wm.start()
    # t = threading.Thread(target=qqBotCenter.continueLogin, args=(groups,kwargs))
    # t.setDaemon(True)
    # t.start()#不能join，join就堵塞了，无法返回

    # 多进程： windows上开不起来？？？
    # p = multiprocessing.Process(target=qqBotCenter.continueLogin, args=(groups,kwargs))
    # p.start()
    # p.join()

    kwargs = None
    pool = multiprocessing.Pool()
    result = Queue.Queue()

    '''
    将子进程对象存入队列中。
    '''
    q.put(pool.apply_async(qqBotCenter.getQRCodeUrl, args=()))  # 维持执行的进程总数为10，当一个进程执行完后添加新进程.
    '''
    因为这里使用的为pool.apply_async异步方法，因此子进程执行的过程中，父进程会执行while，获取返回值并校验。
    '''
    while True:
        kwargs = result.get().get()
        if kwargs:
            pool.terminate()  # 结束进程池中的所有子进程。
            break
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