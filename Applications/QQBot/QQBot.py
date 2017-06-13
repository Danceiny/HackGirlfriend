# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
# from PackageNormalData import *
from flask import Blueprint, request, jsonify, redirect, template_rendered,g,render_template
import requests
import urllib
import os
from contextlib import contextmanager
from Libraries.Utils import *

# 实例化一个blueprint
QQBot = Blueprint("QQBot", __name__)

from Platform.QQBotCenter.QQBotCenter import QQBotCenter

# q = QQBotCenter.instance()

# @QQBot.before_request()
# def getQRCode():
#     g.q = QQBotCenter.instance()
#     g.q.getLoginQRCode()
#
#
# @QQBot.teardown_request()
# def login_after_request(exception):
#     q = getattr(g,'q',None)
#     if q is not None:q.login()
# @allow_cross_domain
# @package_json_request_data

@QQBot.route('qqbot/login',methods = ['POST','GET'],endpoint='loginPage')
@check_api_cost_time
def loginPage():
    # get code pic
    # show login page
    # todo some stuff
    # if q.getLoginQRCode():
    # # if os.path.exists('./img/erweima.login.png'):
    # return os.path.realpath(__file__)
    # os.chdir(os.path.realpath(__file__))
    if type(render_template('index.html'))=='dict':
        return 'false, fuck!'
    else:
        return render_template('index.html')
    # return 'hello world'# + str(render_template('index.html'))
    # return render_template('index.html',entry=contextmanager)

    # return 'hello world'

