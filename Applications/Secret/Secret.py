# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
# from PackageNormalData import *
from flask import Blueprint, request, jsonify, redirect, render_template

from Libraries.Utils import *

from Platform.SecretCenter.SecretCenter import SecretCenter
secretCenter = SecretCenter.instance()
# 实例化一个blueprint
Secret = Blueprint("Secret", __name__)

# @Secret.route('api/v1/nimings/io',methods=['GET'],endpoint='')
@Secret.route('api/v1/nimings/io',methods=['GET'],endpoint='')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def niming(words):
    result = {'code':ED.no_err,'data':{}}
    data = request.data
    if data != None:

        if data['action'] == 'login':
            result = {'code':ED.err_password}
            # data = {'phone_md5':'','password_md5':''}
            info = secretCenter.get_user_info(data.get('phone_md5'))
            if len(info)>0 and info['password_md5'] == data.get('password_md5'):
                result['code'] == ED.no_err # status
            response = jsonify(result)
            if result['code'] == ED.no_err:
                pass #TODO:token
                # token = secret_make_token(info)
                # result['token'] == token
                # response.set_cookie('_user_token_',token)

        elif data['action'] == 'send_pass':
            # 向该号码发送短信验证码
            result = secretCenter.send_pass(data['phone'])
            pass

        elif data['action'] == 'upload_contact':
            # data = {'phone_md5':'','token':'','contacts':[{'phone_md5':''},{'phone_md5':''}]
            # TODO:check token
            result = secretCenter.upload_contact(data)
            pass
        elif data['action'] == 'timeline':
            # data = {phone_md5:'',token:'',page:'',perpage:''}
            result = secretCenter.get_timeline(data)
            pass
        elif data['action'] == 'get_comment':
            # data = {phone_md5:'',token:'',page:'',perpage:'',msgId:''}
            result = secretCenter.get_comment(data)
            pass
        elif data['action'] == 'publish':
            # data = {phone_md5:'',token:'',msg:''}
            result = secretCenter.publish_msg(data)
            pass
        elif data['action'] == 'pub_comment':
            # data = {phone_md5:'',token:'',content:'',msgId:''}
            result = secretCenter.pub_comment(data)
            pass
        else:
            result['code'] == ED.err_params
    else:
        result['code'] = ED.err_sys
    return json.dumps(result)


