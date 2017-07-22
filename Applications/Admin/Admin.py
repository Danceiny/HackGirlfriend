# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from Libraries.Utils import *
from flask import Blueprint, request, jsonify, redirect,render_template,url_for


from Libraries.Utils import *
from Libraries.ErrorDefine import *

# 实例化一个blueprint
Admin = Blueprint("Admin", __name__,template_folder='templates',static_folder='static',static_url_path='admin/static')

@Admin.route('/',methods=['GET'],endpoint='admin_hello_world')
def hello_world():
    return redirect('index')

@Admin.route('index',methods=['GET'],endpoint='admin_index')
@check_api_cost_time
@allow_cross_domain
def index():
    lazy_js_path = url_for('static',filename='js/lazysizes.min.js')
    static_css =  url_for('.static', filename="css/style.css")
    admin_static_css = url_for('Admin.static', filename="css/style.css")
    return render_template('index.html',lazy_js_path=lazy_js_path,static_css=static_css,admin_static_css=admin_static_css)