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
import multiprocessing
# 实例化一个blueprint
QQBot = Blueprint("QQBot", __name__,template_folder='templates',static_folder='static')

from Platform.QQBotCenter.QQBotCenter import QQBotCenter,oneclickstart

qqBotCenter = QQBotCenter.instance()
import threading
import thread
@QQBot.route('qqbot/oneclickstart',methods=['GET'],endpoint='oneclickstart')
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
        for k,v in data.items():
            print 'get params',k,v
            groups.append(str(data[k]))
    print 'groups',groups
    thread.start_new_thread(qqBotCenter.oneclickstart,(groups,))

    # 多进程： windows上开不起来？？？
    # p = multiprocessing.Process(target=oneclickstart, args=())
    # p.start()
    # p.join()

    vpath_url = url_for("static",filename="imaqrcode.png")
    return render_template('QRCode.html',img_vrcode=vpath_url),200,{"Cache-Control": "no-cache, no-store, must-revalidate"}
    # return redirect(vpath_url)

