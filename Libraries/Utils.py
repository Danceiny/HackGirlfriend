#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import request, make_response, jsonify
from functools import wraps
import platform
if 'Win' not in platform.platform():
    pass
import Libraries.ErrorDefine as ED
import datetime
import time
import json
import re
import pytz
import uuid
import traceback
import os
from urllib2 import urlopen
from urllib2 import HTTPError
from Platform.LogCenter.LogCenter import LogCenter
logger = LogCenter.instance().get_logger('UtilsLog')


##################     文件相关      ##################
def concat_dirs(is_abs=False,*dirs):
    '''
    将多级目录连接起来，os.path.join()的迭代版本, 可用..表示上层目录
    :param dirs:
    :return:
    '''
    joined_path = ''
    for dir in dirs:
        if dir != '..':
            joined_path = os.path.join(joined_path,dir)
        elif dir == '..':
            joined_path = os.path.dirname(joined_path)
    if joined_path.endswith(('/','\\')):
        joined_path = joined_path[:-1]
    return os.path.abspath(joined_path) if is_abs else joined_path
##################     文件相关      ##################



# MAC ADDRESS
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
def getCountryCode(ipAddress):
    try:
        response = urlopen("http://freegeoip.net/json/"+ipAddress).read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get("country_code")
def dotip2int(dotip):
    # import socket,struct
    # return socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip)))[0]) 
    return (lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])]))(dotip)

def int2dotip(ip):
    return (lambda x: '.'.join([str(x/(256**i)%256) for i in range(3,-1,-1)]))(ip)


def add_cross_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = "REFERER_URL,Accept,Origin,User-Agent"
    # response.headers['Access-Control-Allow-Credentials']  = 'true'
    return response


# 跨域装饰器
def allow_cross_domain(method):
    @wraps(method)
    def _decorator(*args, **kwargs):
        try:
            rst = make_response(method(*args, **kwargs))
            return add_cross_headers(rst)
        except Exception,e:
            logger.error(repr(traceback.format_exc()))
            return jsonify({'code': ED.err_sys})

    return _decorator

##########################################
# 时间相关 Start
##########################################
def convert_int_2_string_single(int_time, onlydate=False, only_m_d=False):
    key_time = time.localtime(int_time)
    if onlydate == True:
        return time.strftime('%Y-%m-%d', key_time)
    elif only_m_d == True:
        return time.strftime('%m-%d', key_time)
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S', key_time)


# 将int类型时间转成字符串
def convert_int_2_string(datas, keys, onlydate=False, only_m_d=False):
    if type(datas) == dict:
        datas = [datas]
    if type(datas) != list:
        return datas
    if type(keys) == str or type(keys) == unicode:
        keys = [keys]
    if type(keys) != list:
        return datas
    for data in datas:
        for key in keys:
            if data.has_key(key) and type(data[key]) == int:
                key_time = time.localtime(data[key])
                if onlydate == True:
                    data[key] = time.strftime('%Y-%m-%d', key_time)
                elif only_m_d == True:
                    data[key] = time.strftime('%m-%d', key_time)
                else:
                    data[key] = time.strftime('%Y-%m-%d %H:%M:%S', key_time)
    return datas


# 讲 string 时间转化为int
def convert_string_2_int(timestring):
    # if type(timestring) == str or type(timestring) == unicode:
    #     return 0
    return time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S'))


# 将Datetime类型转成字符串
def convert_datetime_2_string(datas, keys, onlydate=False, only_m_d=False):
    if type(datas) == dict:
        datas = [datas]
    if type(datas) != list:
        return datas
    if type(keys) == str or type(keys) == unicode:
        keys = [keys]
    if type(keys) != list:
        return datas
    for data in datas:
        for key in keys:
            if data.has_key(key) and type(data[key]) == datetime.datetime:
                if onlydate == True:
                    data[key] = data[key].strftime('%Y-%m-%d')
                elif only_m_d == True:
                    data[key] = data[key].strftime('%m-%d')
                else:
                    data[key] = data[key].strftime('%Y-%m-%d %H:%M:%S')
    return datas


def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S.000Z'):
    local_tz = pytz.timezone('Asia/Chongqing')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return int(time.mktime(time.strptime(time_str, local_format)))


def get_now_time_int():
    return int(time.time())


def get_now_time_str_ms():
    return ("%.3f" % (time.time())).decode('utf-8')


# api调用耗时
def check_api_cost_time(method):
    @wraps(method)
    def _decorator(*args, **kwargs):
        try:
            start = time.time()
            ret = method(*args, **kwargs)
            end = time.time()
            print method.__name__ + " api cost time %f s" % (end - start)
            # logger.debug(method.__name__ + " api cost time %f s" % (end - start))
            return ret
        except Exception, e:
            logger.error(repr(traceback.format_exc()))
            # return package_ret_data_from_server({'code': 99999})
            return {'code': 99999}

    return _decorator

##########################################
#  时间相关 End                           #
##########################################


#
# # 检查访问是否重复
# def check_api_repeate_access(method):
#     @wraps(method)
#     def _decorator(*args, **kwargs):
#         try:
#             if request.method == "POST":
#                 raw_data = request.data
#                 data = package_data_from_client_json_post_by_str(raw_data)
#                 if not data:
#                     raw_data = request.cookies.get('_UserData_') or request.form.get('secdata') or request.args.get(
#                         "secdata")
#                     data = package_data_from_client_json_post_by_str(raw_data)
#                     data['_params_'] = request.data
#             elif request.method == "GET":
#                 raw_data_cookies = request.cookies.get('_UserData_')
#                 data_cookies = None
#                 if len(raw_data_cookies or '') > 0:
#                     data_cookies = package_data_from_client_json_get_by_str(raw_data_cookies)
#
#                 raw_data = request.args.get("secdata")
#                 if len(raw_data or '') > 0:
#                     data = package_data_from_client_json_get_by_str(raw_data)
#                     if data and data_cookies and data.get('time_stamp', 0) < data_cookies.get('time_stamp', 0):
#                         raw_data = raw_data_cookies
#                         data.update(data_cookies)
#                 else:
#                     raw_data = raw_data_cookies
#                     data = data_cookies
#             else:
#                 raw_data = None
#                 data = None
#
#             if raw_data is not None:
#                 expired_time = 86400  # 过期时间
#                 # 检查请求是否过期，以东八区（即北京时间）为准【北京偏移时间为28800秒】
#                 now_time = int(time.time())
#                 request_time = int(data.get('time_stamp', 0))
#                 if abs(now_time - request_time) > expired_time:
#                     logger.error("access expired. now=[%d], data=[%s]" % (now_time, repr(data)))
#                     return package_ret_data_from_server({'code': ED.err_access_expired,
#                                                          'msg': Text.get(ED.Message[ED.err_access_expired],
#                                                                          data.get('lan', 'en'))})
#
#                 # 检查请求是否重复
#                 md5_sign = md5.new(raw_data).hexdigest()
#                 if mc_light.get(md5_sign) is not None:
#                     logger.error("access repeate. md5=[%s], data=[%s]" % (md5_sign, repr(data)))
#                     return package_ret_data_from_server({'code': ED.err_access_repeate,
#                                                          'msg': Text.get(ED.Message[ED.err_access_expired],
#                                                                          data.get('lan', 'en'))})
#                 else:
#                     mc_light.set(md5_sign, "1", expired_time * 2)
#
#             if data is not None:
#                 if data.has_key('lan'):
#                     data['lan'] = data['lan'].replace('-', '_')
#
#                 request.data = data
#                 lan = data.get('lan', 'en')
#
#                 # 检查用户是否在黑名单
#                 # if securityCenter.check_data_in_black(data):
#                 #     return package_ret_data_from_server({'code':ED.err_user_in_black_list, 'msg':Text.get(ED.Message[ED.err_user_in_black_list], lan)})
#             else:
#                 lan = 'en'
#
#             ret = method(*args, **kwargs)
#             if ret['code'] != ED.no_err and not ret.has_key("msg"):
#                 # 如果返回Code不为200，且无错误信息返回，这里统一设定信息
#                 ret['msg'] = Text.get(ED.Message[ret['code']], lan)
#             elif ret.has_key('flask_response'):
#                 return ret['flask_response']
#             # return package_ret_data_from_server(ret)
#             return ret
#         except Exception, e:
#
#             pass
#             # try:
#             #     if data is not None:
#             #         logger.error(repr(data))
#             # except Exception, e:
#             #     pass
#             # logger.error(repr(traceback.format_exc()))
#             # return package_ret_data_from_server({'code': ED.err_sys})
#
#     return _decorator
def getHostnameOfUrl(url):
    # (?xi)\A
    # [a - z][a - z0 - 9 +\-.] *: //  # Scheme
    # ([a - z0 - 9\-._
    # ~ %!$ & '()*+,;=]+@)?           # User
    # ([a - z0 - 9\-._
    # ~ %]+                           # Named or IPv4 host
    # | \[[a - z0 - 9\-._
    # ~ %!$ & '()*+,;=:]+\])          # IPv6+ host
    reobj = re.compile(r"(?xi)\A[a-z][a-z0-9+\-.]*://([a-z0-9\-._~%!$&'()*+,;=]+@)?([a-z0-9\-._~%]+|[a−z0−9\-.])")
    return reobj.search(url).group(2)


# 获取IP
def getClientRemoteIP(request):
    if request.headers.get('x-forwarded-for') == None:
        return request.environ.get('REMOTE_ADDR')
    else:
        ipStr = request.headers.get('X-Forwarded-For')
        ips = ipStr.split(', ')
        ret = ips[0]
        for ip in ips:
            bis = ip.split('.')
            count = 0
            for bi in bis:
                count = count * 1000 + int(bi)
            if 10000000000 <= count and count <= 10255255255:
                continue
            if 172016000000 <= count and count <= 172131255255:
                continue
            if 192168000000 <= count and count <= 192168255255:
                continue
            ret = ip
            break
        return ret
# 获取本地IP地址
def getLocalIP(outside=True):
    import socket, fcntl, struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if outside == True:
        inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', "eth1"[:15]))
        return socket.inet_ntoa(inet[20:24])
    else:
        inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', "eth0"[:15]))
        return socket.inet_ntoa(inet[20:24])

def package_json_request_data(method):
    @wraps(method)
    def _decorator(*args, **kwargs):
        try:
            if request.method == "POST":
                request.data = json.loads(request.data)
            else:
                temp_raw_data = request.args.items()
                temp_raw_map = {}
                for temp_item in temp_raw_data:
                    temp_raw_map[temp_item[0]] = temp_item[1]
                request.data = temp_raw_map
            request.data['ip'] = getClientRemoteIP(request)
            ret = method(*args, **kwargs)
            return ret
        except Exception, e:
            logger.error(repr(traceback.format_exc()))
            return "%s package_json_request_data error" % str(request)

    return _decorator


##########################################
# 管理后台令牌相关
##########################################
ADMIN_TOKEN_EXPIRED = 8640000

def secret_make_token():
    pass#TODO
    return ''

def admin_check_login():
    token = request.cookies.get('_admin_token_') or request.args.get('_admin_token_')
    if len(token or '') <= 0:
        return False

    token = package_data_fromclient_json_post_boss(token, app_key="token")
    if token:
        if token.get('token_time', 0) + int(token.get('token_expired', ADMIN_TOKEN_EXPIRED)) < int(time.time()):
            # 令牌过期
            return False
        # elif token.get('ua') != request.user_agent.string:
        #     # 此令牌不是这台设备获取的
        #     return False
        else:
            from AdminCenter.BossUserCenter.BossUserCenter import BossUserCenter
            info = BossUserCenter.instance().get_boss_user_info(token['username'])
            if len(info) > 0:
                token.update(info)
                request.admin_token = token
                return True
    return False


def admin_make_token(data):
    token_data = {
        "username": data['username'],
        "token_time": int(time.time()),
        "ua": request.user_agent.string
    }
    if data.has_key('token_expired'):
        token_data['token_expired'] = int(data['token_expired'])
    return package_data_toserver_json_post_boss(token_data, app_key="token")


def admin_check_auth(permission, *args, **kwds):
    def real_decorator(method):
        @wraps(method)
        def wrapped(*args, **kwds):
            if admin_check_login():
                if len(permission) == 0:
                    # 不需要权限
                    return method(*args, **kwds)
                userpermission = request.admin_token['permission']
                # 检查权限
                if 'all' in userpermission or int(permission) in userpermission:
                    return method(*args, **kwds)
            return jsonify({"code": ED.err_no_auth})

        return wrapped

    return real_decorator


##########################################
# 用户令牌相关
##########################################
USER_TOKEN_EXPIRED = 864000


def user_make_token(data):
    token_data = {
        "id_number": data['id_number'],
        "token_time": int(time.time()),
        "ua": request.user_agent.string
    }
    if data.has_key('token_expired'):
        token_data['token_expired'] = int(data['token_expired'])
    return package_data_toserver_json_post_boss(token_data, app_key="user_token")


def check_user_token(method):
    @wraps(method)
    def _decorator(*args, **kwargs):
        return method(*args, **kwargs)
        # result = {"code":ED.err_user_not_login}
        # try:
        #     token = request.headers.get('_cecctm_token_') or request.cookies.get('_cecctm_token_') or request.args.get('_cecctm_token_') or request.form.get('_cecctm_token_')
        #     if len(token or '') <= 0:
        #         return result
        #     token = package_data_fromclient_json_post_boss(token, app_key="user_token")
        #     if token:
        #         if token.get('token_time', 0) + int(token.get('token_expired', USER_TOKEN_EXPIRED)) < int(time.time()):
        #             # 令牌过期
        #             return result
        #         # elif token.get('ua') != request.user_agent.string:
        #         #     # 此令牌不是这台设备获取的
        #         #     return result
        #         else:
        #             request.data['token_time'] = token['token_time']
        #             request.data['id_number'] = token['id_number']  # 把请求中的id_number替换为token中的id_number
        #             return method(*args, **kwargs)
        # except Exception, e:
        #     logger.error(repr(traceback.format_exc()))
        #     result['code'] = ED.err_sys
        # return result

    return _decorator