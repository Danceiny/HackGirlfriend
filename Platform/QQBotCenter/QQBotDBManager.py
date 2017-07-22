#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
from Libraries.Singleton.Singleton import Singleton
import Libraries.ErrorDefine as ED

from Libraries.DBModel import *
from Platform.ConfigCenter.ConfigCenter import ConfigCenter
from Platform.LogCenter.LogCenter import LogCenter
from Libraries.Utils import *


@Singleton
class QQBotDBManager():
    def __init__(self):
        self.logger = LogCenter.instance().get_logger('QQBotCenterLog')
        self.db_model = DBModelFactory.instance().get_db_model()
        # self.db_model_read = DBModelFactory.instance().get_db_model(readonly=True)

        # self.table_name_user = self.conf.get('RDS', 'table_name_zuiwan_user')
        # self.table_name_user_count = self.conf.getint('RDS', 'table_name_zuiwan_user_count')
        # self.table_name_user_keys = json.loads(self.conf.get('RDS', 'table_name_zuiwan_user_keys'))
        self.table_name_user = "qqbot_user"
        self.table_name_user_count = 1
        self.table_name_user_keys = ('qq_number', 'watch_group', 'login_records', 'nick_name')

        self.table_name_records = "qqbot_records"
        self.table_name_records_count = 1
        self.table_name_records_keys = ('msgId','up_msgId','down_msgId','content','to_qqNumber','timestamp','pollType')


############## user part #################
    def get_users_list(self, data):
        limit_count = int(data.get('count', 10))
        select_sql = DBModel.sql_select(self.table_name_user,
        keys=data.get('keys',self.table_name_user_keys),
        limit='0,%d' % limit_count, order=[{'key': 'last_login', 'desc': True}])
        records = self.db_model.GetList(select_sql)
        return records

    def get_user_detail(self, data):
        qq_number = int(data['qq_number'])
        where_condition = DBModel.sql_and({"qq_number": qq_number})
        sql = DBModel.sql_select(self.table_name_user, where=where_condition)
        records = self.db_model.GetOne(sql)
        return records

    def get_user_records(self,data):
        to_qqNumber = int(data['qq_number'])
        where_condition = DBModel.sql_and({"to_qqNumber": to_qqNumber})
        sql = DBModel.sql_select(self.table_name_records, where=where_condition)
        records = self.db_model.GetList(sql)
        return records

    def add_records(self,data):
        result = {'code': ED.no_err}
        if not 'msgId' in data or len(data.get('msgId','')) <= 0:
            data['msgId'] = get_now_time_str_ms().replace('.', '')  # like '1497257116332'
        if not 'timestamp' in data or data.get('timestamp',0) == 0:
            data['timestamp'] = get_now_time_int()
        else:
            return {'code':ED.err_params}
        sql = self.db_model.sql_insert(table=self.table_name_records, data=data, keys=self.table_name_records_keys)
        flag = self.db_model.execute(sql)
        if flag == None or flag.rowcount <= 0:
            result['code'] = ED.unknown_err
        result['data'] = {'msgId':data['msgId']}
        return result

    def add_user(self, data):
        '''
        :param data {}
        :return:
        '''
        result = {'code': ED.no_err}
        if not 'zuser_id' in data or len(data.get('zuser_id','')) <= 0:
            data['zuser_id'] = get_now_time_str_ms().replace('.', '')  # like '1497257116332'
        if not 'create_time' in data or data.get('create_time',0) == 0:
            data['create_time'] = get_now_time_int()
        else:
            return {'code':ED.err_params}
        sql = self.db_model.sql_insert(table=self.table_name_user, data=data, keys=self.table_name_user_keys)
        flag = self.db_model.execute(sql)
        if flag == None or flag.rowcount <= 0:
            result['code'] = ED.unknown_err
        return result

    def delete_user(self,data):
        result = {'code':ED.no_err}
        try:
            sql_delete_user = ""
            if 'zuser_id' in data:
                sql_delete_user = DBModel.sql_delete(self.table_name_user,where=DBModel.sql_and({'zuser_id':data['zuser_id']}))
            elif 'nick_name' in data:
                sql_delete_user = DBModel.sql_delete(self.table_name_user,where=DBModel.sql_and({'nick_name':data['nick_name']}))
            else:
                return {'code':ED.err_params}
            ret_del = self.db_model.execute(sql_delete_user)
            if ret_del == None:
                result['code'] = ED.err_sys
        except Exception,e:
            self.logger.error("ZuiwanCenter delete user error, sql=[%s],msg=[%s]" % (repr(sql_delete_user),repr(e)))
            result['code'] = ED.err_sys
        return result

    def update_user(self,data,params=None):
        result = {'code':ED.no_err}
        if params == None or len(params) == 0:
            params = self.table_name_user_keys
        try:
            sql_update_user = DBModel.sql_update(self.table_name_user,data,where=DBModel.sql_and({'zuser_id':data['zuser_id']}),keys=params)
            flag = self.db_model.execute(sql_update_user)
            if flag == None:
                result['code'] = self.add_user(data)['code']
        except Exception,e:
            self.logger.error("ZuiwanCenter update user error. sql=[%s],msg=[%s]" % (repr(sql_update_user),repr(e)))
            result['code'] = ED.err_sys
        return result



############ meeting part ################
    def get_meetings_list(self,data):
        pass

    def get_meeting_info(self,data):
        pass

    def add_meeting(self,data):
        result = {'code': ED.no_err}
        if not 'meeting_id' in data or len(data.get('meeting_id') or '') <= 0:
            data['meeting_id'] = get_now_time_str_ms().replace('.', '')  # like '1497257116332'
        sql = self.db_model.sql_insert(table=self.table_name_meeting, data=data, keys=self.table_name_meeting_keys)
        flag = self.db_model.execute(sql)
        if flag == None or flag.rowcount <= 0:
            result['code'] = ED.unknown_err
        return result

    def delete_meeting(self,data):
        result = {'code':ED.no_err}
        if 'meeting_id' in data:
            sql_delete_meeting = DBModel.sql_delete(self.table_name_meeting,where=DBModel.sql_and({'meeting_id':data['meeting_id']}))
        else:
            return {'code':ED.err_params}
        try:
            ret_del = self.db_model.execute(sql_delete_meeting)
            if ret_del == None:
                result['code'] = ED.err_sys
        except Exception,e:
            self.logger.error("ZuiwanCenter delete meeting error, sql=[%s],msg=[%s]" % (repr(sql_delete_meeting),repr(e)))
            result['code'] = ED.err_sys
        return result

    def update_meeting(self,data,params=None):
        result = {'code':ED.no_err}
        if params == None or len(params) == 0:
            params = self.table_name_keys
        try:
            sql_update_meeting = DBModel.sql_update(self.table_name_user,data,where=DBModel.sql_and({'meeting_id':data['meeting_id']}),keys=params)
            flag = self.db_model.execute(sql_update_meeting)
            if flag == None:
                result['code'] = self.add_user(data)['code']
        except Exception,e:
            self.logger.error("ZuiwanCenter update meeting error. sql=[%s],msg=[%s]" % (repr(sql_update_meeting),repr(e)))
            result['code'] = ED.err_sys
        return result

    def get_next_meeting_leave_list(self,data):
        pass
    def get_last_meeting_leave_list(self,data):
        pass

    def get_leave_list(self,data):
        result = {'code':ED.no_err}
        pass



