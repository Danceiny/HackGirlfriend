#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import request, make_response, jsonify
from functools import wraps
# from MyCrypto import *
#import ErrorDefine as ED
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

def delay(delay_time):
    for i in xrange(delay_time):
        pass

def pass_time(initTime):
    rs = (time.time() - initTime)
    initTime = time.time()
    return initTime,str(round(rs, 3))

def get_ts():
    ts = time.time()
    while ts < 1000000000000:
        ts = ts * 10
    ts = int(ts)
    return ts
def getQRtoken(qrsig):
    e = 0
    for i in qrsig:
        e += (e << 5) + ord(i)
    return 2147483647 & e

#Encryption Algorithm Used By QQ
def gethash(selfuin, ptwebqq):
    selfuin += ""
    N=[0,0,0,0]
    for T in range(len(ptwebqq)):
        N[T%4]=N[T%4]^ord(ptwebqq[T])
    U=["EC","OK"]
    V=[0, 0, 0, 0]
    V[0]=int(selfuin) >> 24 & 255 ^ ord(U[0][0])
    V[1]=int(selfuin) >> 16 & 255 ^ ord(U[0][1])
    V[2]=int(selfuin) >>  8 & 255 ^ ord(U[1][0])
    V[3]=int(selfuin)       & 255 ^ ord(U[1][1])
    U=[0,0,0,0,0,0,0,0]
    U[0]=N[0]
    U[1]=V[0]
    U[2]=N[1]
    U[3]=V[1]
    U[4]=N[2]
    U[5]=V[2]
    U[6]=N[3]
    U[7]=V[3]
    N=["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    V=""
    for T in range(len(U)):
        V+= N[ U[T]>>4 & 15]
        V+= N[ U[T]    & 15]
    return V




def date_to_millis(d):
    return int(time.mktime(d.timetuple())) * 1000

def CProcess(content):
    return str(content.replace("\\", r"\\").replace("\n", r"\n").replace("\r", r"\r").replace("\t", r"\t").replace('"', r'\"'))


def thread_exist(tuin,ThreadList):
    for t in ThreadList:
        if t.isAlive():
            if t.tuin == tuin:
                t.check_msg()
                return t
        else:
            ThreadList.remove(t)
    return False


def group_thread_exist(gid,GroupThreadList):
    for t in GroupThreadList:
        if str(t.gid) == str(gid):
            return t
    return False