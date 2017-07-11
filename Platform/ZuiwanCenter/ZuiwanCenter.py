#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from Libraries.Singleton.Singleton import Singleton
from Platform.LogCenter.LogCenter import LogCenter
import Libraries.ErrorDefine as ED
from Libraries.Utils import *
from ZuiwanDBManager import ZuiwanDBManager

# Descripion

@Singleton
class ZuiwanCenter(object):
    def __init__(self):
        self.logger = LogCenter.instance().get_logger('ZuiwanCenterLog')
        self.zuiwanDBManager = ZuiwanDBManager.instance()

#################   user part  #########################
    def get_user_detail(self,data):
        ret_info = {'code': ED.no_err, 'data': {}}
        if not 'zuser_id' in data and not 'nick_name' in data:
            ret_info['code'] = ED.err_params
        else:
            ret_info['data'] = self.zuiwanDBManager.get_user_detail(data=data)
        return ret_info

    def get_users_list(self,data):
        return self.zuiwanDBManager.get_users_list(data)

    def update_user(self,data):
        ret = self.zuiwanDBManager.update_user(data=data,params=data.get('update_keys',[]))#向服务器post需要修改的字段数组
        return ret


    def add_user(self,data):
        ret_info = {'code':ED.no_err,'data':{}}
        if 'zuser_id' not in data:
            data['zuser_id'] = get_now_time_str_ms().replace('.', '')   #关联关键字表需要a_id
        ret_info['code'] = self.zuiwanDBManager.add_user(data)['code']    #这里只返回errcode
        ret_info['data']['zuser_id'] = data['zuser_id']
        return ret_info


    def find_user(self, data):
        result = {'code': ED.no_err}
        if 't' in data and 'c' in data:  # also: set(['t','c']).issubset(data)
            result['data'] = self.zuiwanDBManager.find_user(data)
        else:
            result['code'] = ED.err_params
        return result

    def delete_user(self,data):
        ret_del = self.zuiwanDBManager.delete_user(data)
        return ret_del


#####################  meeting part    ########################
    def get_leave_list(self,data):
        data['count'] = data.get('count',5) #获取最近count次会议到会情况和下一次会议请假情况
        return self.newsDBManager.get_leave_list(data)
    def get_next_meeting_leave_list(self,data):
        pass
    def get_last_meeting_leave_list(self,data):
        pass


###################   vote part       ######################
    def get_vote(self,data):
        result = {'code':ED.no_err}
        if not 'event' in data:
            result['code'] = ED.err_params
        else:
            result['data'] = self.zuiwanDBManager.get_vote(data)
        return result

    def add_vote(self,data):
        result = {'code':ED.no_err}
        if not 'event' in data:
            result['code'] = ED.err_params
        else:
            result['data'] = self.zuiwanDBManager.add_vote(data)
        return result