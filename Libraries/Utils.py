#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import request, make_response, jsonify
from functools import wraps
# from MyCrypto import *
import ErrorDefine as ED
import hashlib
import md5
import datetime
import time
import traceback
import urlparse
import json
import urllib2
import re
import random
import pytz
import uuid

# MAC ADDRESS
def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


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
        except Exception, e:
            # logger.error(repr(traceback.format_exc()))
            return jsonify({'code': ED.err_sys})

    return _decorator

def convert_int_2_string_single(int_time,onlydate=False,only_m_d=False):
    key_time = time.localtime(int_time)
    if onlydate == True:
        return time.strftime('%Y-%m-%d', key_time)
    elif only_m_d == True:
        return time.strftime('%m-%d', key_time)
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S', key_time)

# 将int类型时间转成字符串
def convert_int_2_string(datas, keys, onlydate=False,only_m_d=False):
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
                    data[key] = time.strftime('%Y-%m-%d',key_time)
                elif only_m_d == True:
                    data[key] = time.strftime('%m-%d',key_time)
                else:
                    data[key] = time.strftime('%Y-%m-%d %H:%M:%S',key_time)
    return datas

#讲 string 时间转化为int
def convert_string_2_int(timestring):
    # if type(timestring) == str or type(timestring) == unicode:
    #     return 0
    return time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S'))

# 将Datetime类型转成字符串
def convert_datetime_2_string(datas, keys, onlydate=False,only_m_d=False):
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