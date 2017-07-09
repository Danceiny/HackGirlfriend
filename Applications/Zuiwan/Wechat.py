# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
# from PackageNormalData import *
from flask import Blueprint, request, jsonify, redirect, render_template
import requests
import urllib
from Libraries.Utils import *
from Platform.ZuiwanCenter.ZuiwanCenter import ZuiwanCenter
zuiwanCenter = ZuiwanCenter.instance()
# 实例化一个blueprint
ZuiwanWechat = Blueprint("ZuiwanWechat", __name__)



@ZuiwanWechat.route('api/v1/zuiwan/ask-leave', methods = ['POST'], endpoint='ask_leave')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def ask_leave():
    result = {'code':ED.no_err,'data':{}}
    data = request.data
    # data = [{user:'',ask_time:'',token:''}]
    result['data'] = zuiwanCenter.ask_leave(data)
    return json.dumps(result)

@ZuiwanWechat.route('api/v1/zuiwan/vote', methods = ['POST'], endpoint='zuiwan_vote')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def zuiwan_vote():
    result = {'code':ED.no_err,'data':{}}
    data = request.data
    if data != None:
        result['data'] = zuiwanCenter.vote(data)
    else:
        result['code'] = ED.err_sys

    return json.dumps(result)


@ZuiwanWechat.route('api/v1/zuiwan/get-vote', methods = ['GET'], endpoint='zuiwan_get_vote')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def zuiwan_vote():
    result = {'code':ED.no_err,'data':{}}
    data = request.data
    if data != None:
        result['data'] = zuiwanCenter.get_vote(data)
    else:
        result['code'] = ED.err_sys

    return json.dumps(result)