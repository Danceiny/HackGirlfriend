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
QQBot = Blueprint("QQBot", __name__,template_folder='templates',static_folder='static')

from Platform.QQBotCenter.QQBotCenter import QQBotCenter

qqBotCenter = QQBotCenter.instance()

import threading
import thread
@QQBot.route('qqbot/oneclickstart',methods=['GET'],endpoint='oneclickstart')
@check_api_cost_time
@allow_cross_domain
def oneclickstart():
    result = {'code':ED.no_err}
    # data = request.data
    # template = url_for('qrcode','/Applications/static/templates/QRCode.html')
    # thread.start_new_thread(qqBotCenter.oneclickstart,())
    # return send_from_directory('Applications/QQBot/templates','QRCode.html')
    # ret = qqBotCenter.getQRCodeUrl()
    # thread.start_new_thread(qqBotCenter.continueLogin,(ret,))
    thread.start_new_thread(qqBotCenter.oneclickstart,())
    vpath_url = url_for("static",filename="imaqrcode.png")
    return render_template('QRCode.html',img_vrcode=vpath_url)
    # return redirect(vpath_url)

