# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
from flask import Blueprint, request, jsonify, redirect, render_template
import requests
import urllib
from Libraries.Utils import *
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

from Libraries.mythreadpool import *




# 实例化一个blueprint
Admin = Blueprint("Admin", __name__,template_folder='templates',static_folder='static',static_url_path='admin/static')

@Admin.route('/',methods=['GET'],endpoint='admin_hello_world')
def hello_world():
    return redirect('admin/index')

@Admin.route('admin/index',methods=['GET'],endpoint='admin_index')
@check_api_cost_time
@allow_cross_domain
def index():
    lazy_js_path = url_for('static',filename='js/lazysizes.min.js')
    img = url_for('Admin.static',filename='images/index.png')
    static_css =  url_for('.static', filename="css/style.css")
    admin_static_css = url_for('Admin.static', filename="css/style.css")

    print static_css,admin_static_css
    return render_template('index.html',lazy_js_path=lazy_js_path,static_css=static_css,admin_static_css=admin_static_css)