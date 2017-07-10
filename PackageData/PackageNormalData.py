#!rusr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import request
import platform
import msgpack
import json

XXTEA_KEY_MAP = {
    "client" : {
        "default" : "JQQjo*m9#vd9O@Ak0c",
        "token" : "mQRkkj$Z*Qjoio*m9",
        "user_token" : "nQRikjqZ*Qjnio*m2",
    },
    "server" : {
        "default" : "lujL#Rkkj$Z*G8G@o6X",
    }
}

def package_ret_data_from_server(data, app_key="default", url_safe=False):  # 将服务器返回信息加密
    xxtea_key = XXTEA_KEY_MAP['server'].get(app_key) or XXTEA_KEY_MAP['server']['default']
    b64func = not url_safe and xx_b64encode or xx_url_b64encode
    return b64func(xxtea_encrypt(msgpack.packb(data), xxtea_key))

def package_data_from_client_json_post(request, app_key="default", url_safe=False): # 将客户端发来的数据解密
    return package_data_from_client_json_post_by_str(request.data, app_key=app_key, url_safe=url_safe)

def package_data_from_client_json_post_by_str(data_str, with_request=True, app_key="default", url_safe=False): # 将客户端发来的数据解密
    if data_str == None or data_str == "":
        return None

    b64func = not url_safe and xx_b64decode or xx_url_b64decode
    xxtea_key = XXTEA_KEY_MAP['client'].get(app_key) or XXTEA_KEY_MAP['client']['default']
    data = xxtea_decrypt(b64func(url_decode(data_str)), xxtea_key)
    if len(data) == 0:
        return None
    else:
        params = msgpack.unpackb(data)
    params['debug'] = bool(params.get('debug', False))
    return _lite_data(params, with_request=with_request)

def package_data_toserver_json_post_boss(data, app_key="default", url_safe=False): # 从后台向服务器发送消息的加密
    xxtea_key = XXTEA_KEY_MAP['client'].get(app_key) or XXTEA_KEY_MAP['client']['default']
    b64func = not url_safe and xx_b64encode or xx_url_b64encode
    return url_encode(b64func(xxtea_encrypt(msgpack.packb(data), xxtea_key)))

def package_data_fromserver_json_post_boss(data, app_key="default", url_safe=False): # 从服务器发向后台的消息的解密
    xxtea_key = XXTEA_KEY_MAP['server'].get(app_key) or XXTEA_KEY_MAP['server']['default']
    b64func = not url_safe and xx_b64decode or xx_url_b64decode
    return msgpack.unpackb(xxtea_decrypt(b64func(data), xxtea_key))

def package_data_fromclient_json_post_boss(data, app_key="default", url_safe=False): # 从客户端发向后台的消息的解密
    xxtea_key = XXTEA_KEY_MAP['client'].get(app_key) or XXTEA_KEY_MAP['client']['default']
    b64func = not url_safe and xx_b64decode or xx_url_b64decode
    return msgpack.unpackb(xxtea_decrypt(b64func(url_decode(data)), xxtea_key))

def package_data_from_client_json_get(request, app_key="default", url_safe=False): # 从客户端发送服务器的GET解密
    return package_data_from_client_json_get_by_str(request.args.get("secdata"), app_key=app_key, url_safe=url_safe)

def package_data_from_client_json_get_by_str(data_str, with_request=True, app_key="default", url_safe=False):
    if data_str == None or data_str == "":
        return None

    xxtea_key = XXTEA_KEY_MAP['client'].get(app_key) or XXTEA_KEY_MAP['client']['default']
    b64func = not url_safe and xx_b64decode or xx_url_b64decode
    data = xxtea_decrypt(b64func(url_decode(data_str)), xxtea_key)
    if len(data) == 0:
        return None
    else:
        params = msgpack.unpackb(data)
    if type(params) != dict:
        return params

    params['debug'] = bool(params.get('debug', False))
    return _lite_data(params, with_request=with_request)

def package_data_dynamic_update(request):
    params={}
    params['id'] = request.form.get("id")
    params['ver'] = request.form.get("ver", "")
    params['operate'] = request.form.get("operate", "")
    params['title'] = request.form.get("title", "")
    params['message'] = request.form.get("message", "")
    params['btn1'] = request.form.get("btn1", "")
    params['btn2'] = request.form.get("btn2", "")
    params['url'] = request.form.get("url", "")
    params['switch'] = request.form.get("switch", "")
    params['apptype'] = request.form.get("apptype", "")
    return _lite_data(params, clearBlank=False)

def _lite_data(data, clearBlank=True, with_request=True):
    delkeys = []
    for key in data:
        if None == data[key] or (clearBlank and type(data[key]) == str and len(str(data[key])) <= 0):
            delkeys.append(key)

    for key in delkeys:
        del data[key]

    if with_request == True:
        from Utils import getClientRemoteIP
        data['ip'] = getClientRemoteIP(request)
    return data

