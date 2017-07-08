# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# from PackageNormalData import *
from flask import Blueprint, request, jsonify, redirect, render_template
from Libraries.Utils import *
from Platform.ZuiwanCenter.ZuiwanCenter import ZuiwanCenter
zuiwanCenter = ZuiwanCenter.instance()
# 实例化一个blueprint
ZuiwanUser = Blueprint("ZuiwanUser", __name__)
# Description

@ZuiwanUser.route('api/v1/zuiwan/user/modify', methods = ['POST','GET'], endpoint='modify-user')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def modify_user():
    result = {'code':ED.no_err,'data':{}}
    data = request.data
    # data = {username:'',create_time:'',password:'',email:'',role:'',...}
    if data != None:
        if data.get('action') == 'add':
            result = zuiwanCenter.add_user(data)
        elif data.get('action') == 'update':
            result = zuiwanCenter.update_user(data)
        elif data.get('action') == 'delete':
            result = zuiwanCenter.delete_user(data)
        else:
            result['code'] = ED.err_params
    else:
        result['code'] = ED.err_sys
    return json.dumps(result)

@ZuiwanUser.route('api/v1/zuiwan/get-users-list', methods = ['GET'], endpoint='get-users-list')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def get_users_list():
    result = {'code':ED.no_err,'data':{}}
    data = request.data
    if data != None:
        result['data'] = zuiwanCenter.get_users_list(data)
    else:
        result['code'] = ED.err_sys
    return json.dumps(result)

@ZuiwanUser.route('api/v1/zuiwan/get-user-detail', methods = ['GET'], endpoint='get-user-detail')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def get_user_detail():
    result = {'code':ED.no_err,'data':{}}
    data = request.data
    if data != None:
        result = zuiwanCenter.get_user_detail(data)
    else:
        result['code'] = ED.err_sys
    return json.dumps(result)

@ZuiwanUser.route('api/v1/zuiwan/find-user', methods = ['GET'], endpoint='find-user')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def find_user():
    result = {'code':ED.no_err,'data':{}}
    data = request.data
    if data != None:
        result = zuiwanCenter.find_user(data)
    else:
        result['code'] = ED.err_sys
    return json.dumps(result)


@ZuiwanUser.route('api/v1/mysql-dbtest',methods=['GET'],endpoint='mysql-dbtest')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def mysql_dbtest():
    result = {'code':ED.no_err,'data':{}}
    data = request.data
    if data != None:
        from Temp.DBtest import DBtest
        dbtest = DBtest.instance()
        if data.get('action') == 'add':
            result = dbtest.insert(data)
        elif data.get('action') == 'update':
            result = dbtest.update(data)
        elif data.get('action') == 'delete':
            result = dbtest.delete(data)
        elif data.get('action') == 'find':
            result = dbtest.select(data)
        else:
            result['code'] = ED.err_params
    else:
        # result['code'] = ED.err_sys
        result['code'] = 'fuckyou'
    return json.dumps(result)