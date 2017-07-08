#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import Libraries.ErrorDefine as ED

from Libraries.Singleton.Singleton import Singleton
from MyConfigParser import ConfigParser

from Libraries.DBModel import *
from Platform.LogCenter.LogCenter import LogCenter

@Singleton
class ConfigCenter(object):
    def __init__(self, conf_file = None):
        self.db_model = DBModelFactory.instance().get_db_model()
        self.db_model_read = DBModelFactory.instance().get_db_model(readonly=True)
        self.logger = LogCenter.instance().get_logger('ExceptionLog')

        self.config_table = 't_cc_configs'

        ret_all_conifgs = self.get_configs()
        if ret_all_conifgs['code'] == ED.no_err:
            self.all_configs = ret_all_conifgs['data']
        else:
            self.all_configs = {}

        self._configs = {}
        for config in self.all_configs:
            if not self._configs.has_key(config['file']):
                self._configs[config['file']] = {}
            if not self._configs[config['file']].has_key(config['section']):
                self._configs[config['file']][config['section']] = {}
            self._configs[config['file']][config['section']][config['key']] = config['value']

    def get_parser(self,file):
        if not self._configs.has_key(file):
            return ConfigParser({}, file)

        return ConfigParser(self._configs[file], file)

    def delete_config(self,data):
        result = {'code': ED.no_err}
        try:
            sql_delete_config = ""
            if data.has_key('id') > 0:
                sql_delete_config = "delete from `%s` where `id`=%d" % (self.config_table, int(data['id']))
            elif data.has_key('section') and len(data['section']) > 0:
                sql_delete_config = "delete from `%s` where `section`='%s'" % (self.config_table, data['section'])
            elif data.has_key('file') and len(data['file']) > 0:
                sql_delete_config = "delete from `%s` where `file`='%s'" % (self.config_table, data['file'])
            ret_del = self.db_model.execute(sql_delete_config)
            if ret_del == None:
                result['code'] = ED.err_sys
        except Exception, e:
            self.logger.error("ConfigCenter delete_config error. sql=[%s],msg=[%s]" % (repr(sql_delete_config),repr(e)))
            result['code'] = ED.err_sys
        return result

    def update_config(self, data):
        result = {'code': ED.no_err}
        try:
            sql_update_config = DBModel.sql_update(self.config_table, data, where=DBModel.sql_and(data, keys=['id']), keys=["file", "key", "section", "value", "type", "remark"])
            ret_update = self.db_model.execute(sql_update_config)
            if ret_update == None:
                result['code'] = ED.err_sys
        except Exception, e:
            self.logger.error("ConfigCenter update_config error. sql=[%s],msg=[%s]" % (repr(sql_update_config),repr(e)))
            result['code'] = ED.err_sys
        return result

    def add_config(self, data):
        result = {'code': ED.no_err}
        try:
            sql_add_config = DBModel.sql_insert(self.config_table, data, keys=["file", "section", "key", "value", "type", "remark"])
            ret_add = self.db_model.execute(sql_add_config)
            if ret_add == None:
                result['code'] = ED.err_sys
        except Exception, e:
            self.logger.error("ConfigCenter add_config error. sql=[%s],msg=[%s]" % (repr(sql_add_config),repr(e)))
            result['code'] = ED.err_sys
        return result


    def get_configs(self,file=None, section=None, key=None, pid=None):
        result = {'code': ED.no_err}
        try:
            where_condition = DBModel.sql_and({
                "file" : file,
                "section" : section,
                "key" : key,
                "id" : pid,
            }, clearblank=True)
            sql_get_config = DBModel.sql_select(self.config_table, where=where_condition)
            ret_get = self.db_model_read.GetList(sql_get_config)
            if ret_get == None or len(ret_get) == 0 :
                result['code'] = ED.err_sys
            else:
                result['data'] = ret_get
        except Exception, e:
            self.logger.error("ConfigCenter get_configs error. msg=[%s]" % repr(e))
            result['code'] = ED.err_sys
        return result