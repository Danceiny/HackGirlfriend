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
class DBtest():
    def __init__(self):
        self.logger = LogCenter.instance().get_logger('ZuiwanCenterLog')
        self.db_model = DBModelFactory.instance().get_db_model()
        self.db_model_read = DBModelFactory.instance().get_db_model(readonly=True)

        # self.table_name_user = self.conf.get('RDS', 'table_name_zuiwan_user')
        # self.table_name_user_count = self.conf.getint('RDS', 'table_name_zuiwan_user_count')
        # self.table_name_user_keys = json.loads(self.conf.get('RDS', 'table_name_zuiwan_user_keys'))
        self.table_name_user = "zuiwan_user"
        self.table_name_user_count = 1
        self.table_name_user_keys = ['zuser_id', 'nick_name', 'email', 'create_time', 'avatar_url', 'credits','role','psw']

        self.table_name_meeting = "zuiwan_meeting"
        self.table_name_meeting_count = 1
        self.table_name_meeting_keys = ['meeting_id','topic','start_time','duration','des','people']
        # 学校相关的信息存储到另一张表，由zuser_id关联

    def select(self, data):
        select_sql = DBModel.sql_select(self.table_name_user,
                                        keys=self.table_name_user_keys,
                                        where=DBModel.sql_and({data.get('queryType',''):data.get('queryContent','')}),
                                        order=[{'key': 'create_time', 'desc': True}])
        print 'dbtest select',select_sql
        records = self.db_model.GetList(select_sql)
        return records

    def insert(self, data):
        result = {'code': ED.no_err}
        if not 'zuser_id' in data or len(data.get('zuser_id') or '') <= 0:
            data['zuser_id'] = get_now_time_str_ms().replace('.', '')  # like '1497257116332'
        if not 'create_time' in data or data.get('create_time',0) == 0:
            data['create_time'] = get_now_time_int()
        else:
            return {'code':ED.err_params}
        sql = self.db_model.sql_insert(table=self.table_name_user, data=data, keys=self.table_name_user_keys)
        print 'dbtest insert',sql
        flag = self.db_model.execute(sql)
        if flag == None or flag.rowcount <= 0:
            result['code'] = ED.unknown_err
        return result

    def delete(self,data):
        result = {'code':ED.no_err}
        try:
            sql_delete_user = ""
            if 'zuser_id' in data:
                sql_delete_user = DBModel.sql_delete(self.table_name_user,where=DBModel.sql_and({'zuser_id':data['zuser_id']}))
            elif 'nick_name' in data:
                sql_delete_user = DBModel.sql_delete(self.table_name_user,where=DBModel.sql_and({'nick_name':data['nick_name']}))
            else:
                return {'code':ED.err_params}
            print sql_delete_user
            ret_del = self.db_model.execute(sql_delete_user)
            if ret_del == None:
                result['code'] = ED.err_sys
        except Exception,e:
            self.logger.error("ZuiwanCenter delete user error, sql=[%s],msg=[%s]" % (repr(sql_delete_user),repr(e)))
            result['code'] = ED.err_sys
        return result

    def update(self,data,params=None):
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

