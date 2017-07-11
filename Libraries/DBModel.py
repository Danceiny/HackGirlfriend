#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
import pymysql
import json
import MySQLdb

from Singleton.Singleton import Singleton
from PackageData.DBConfigs import *

from Platform.LogCenter.LogCenter import LogCenter

logger = LogCenter.instance().get_logger('ExceptionLog')

global base_db_models
if 'base_db_models' not in dir():
    base_db_models = None


def convert_2_string(data):
    data_type = type(data)
    if data_type == dict or data_type == set:
        return json.dumps(data)
    return MySQLdb.escape_string(str(data))


@Singleton
class DBModelFactory():
    def __init__(self):
        global base_db_models
        if base_db_models == None:
            base_db_models = {}
            self.create_db_model(init_db_config)

            # db_model = self.create_db_model(init_db_config)
            # sql = "select `value` from `%s` where `key` = '%s' " % (
            # init_db_config['init_config_table'], init_db_config['init_config_key'])
            # db_configs = db_model.GetOne(sql)
            #
            # assert (db_configs != None, "db_model is none type")
            # db_configs = json.loads(db_configs['value'])
            #
            # for config in db_configs:
            #     self.create_db_model(config)

    # @db_config
    #   name : 数据模型名字，用于区分多个数据库的连接
    #   host : 数据库写地址
    #   host_s : 数据库只读地址，是一个数组
    #   user : 数据库用户名
    #   passwd : 数据库密码
    #   db_name : 数据库名称
    #   port : 数据库端口，默认为3306
    #   charset : 数据库字体集，默认为utf8
    #   cursorclass : 取数据时游标类型，默认为pymysql.cursors.DictCursor（可以自动转为Key-Value的结果集）
    def create_db_model(self, db_config):
        global base_db_models
        db_name = db_config.get('name', 'default')
        if not base_db_models.has_key(db_name):
            # 这个数据操作模型未创建
            base_db_models[db_name] = db_config

        return self.get_db_model(db_name)

    # name : 数据模型名字，用于区分多个数据库的连接
    # readonly : 用来标识要是获取可读写还是只读的数据模型
    def get_db_model(self, name='default', readonly=False):
        global base_db_models
        model = base_db_models.get(name, base_db_models.get('default', None))

        if model is None:
            return None
        db_type = 'db_object' + (readonly and "_r" or "")
        if not model.has_key(db_type):
            model[db_type] = DBModel(model, readonly)

        return model[db_type]


# /**
#  * DBModel.py    基础数据操作类
#  *
#  * @copyright            (C) Graig
#  * @lastmodify            2015-6-6
#  */
class DBModel():
    # 随机选取只读数据库连接
    @staticmethod
    def choose_mysql_host_s(hosts):
        num = random.randint(0, 100)
        total = 0
        for index in range(0, len(hosts)):
            total += hosts[index]['rate']
            if num <= total:
                return hosts[index]['host']

        return hosts[len(hosts) - 1]['host']

    @staticmethod
    def sql_insert(table, data, replace=False, keys=None):
        con = ''
        val = ''
        if keys != None:
            for key in keys:
                if data.has_key(key):
                    con = "%s`%s`, " % (con, str(key))
                    val = "%s'%s', " % (val, convert_2_string(data[key]))
        else:
            for key in data:
                con = "%s`%s`, " % (con, str(key))
                val = "%s'%s', " % (val, convert_2_string(data[key]))
        if replace == True:
            return "replace into `%s`(%s) values(%s)" % (table, con.rstrip(', '), val.rstrip(', '))
        else:
            return "insert into `%s`(%s) values(%s)" % (table, con.rstrip(', '), val.rstrip(', '))

    @staticmethod
    def sql_update(table, data, where=None, keys=None):
        set_con = ''
        if keys != None:
            for key in keys:
                if data.has_key(key):
                    set_con = "%s`%s`='%s', " % (set_con, key, convert_2_string(data[key]))
        else:
            for key in data:
                set_con = "%s`%s`='%s', " % (set_con, key, convert_2_string(data[key]))
        sql = "update `%s` set %s" % (table, set_con.rstrip(', '))
        if where != None and len(where) > 0:
            sql += " where %s" % where
        return sql

    @staticmethod
    def sql_select_string(sql, where=None, limit=None, order=None, group=None):
        if where != None and len(where) > 0:
            if type(where) == list:
                where = " and ".join(where)
            sql += " where %s" % where
        if group != None and len(group) > 0:
            if type(group) == list:
                group_sql = ""
                for group_item in group:
                    group_sql += "`%s`, " % group_item
                sql += " group by %s" % group_sql.rstrip(', ')
            else:
                sql += " group by %s" % group
        if order != None and len(order) > 0:
            if type(order) == list:
                order_sql = ""
                for order_item in order:
                    if type(order_item) == dict:
                        if order_item.get("desc", False) == True:
                            order_sql += "`%s` DESC, " % order_item['key']
                            continue
                        else:
                            order_item = order_item['key']
                    order_sql += "`%s`, " % order_item
                sql += " order by %s" % order_sql.rstrip(', ')
            else:
                sql += " order by %s" % order
        if limit != None and len(str(limit)) > 0:
            sql += " limit %s" % str(limit)
        return sql

    @staticmethod
    def sql_select(table, keys=None, where=None, limit=None, order=None, group=None):
        if keys == None:
            select_keys = '*'
        else:
            select_keys = ""
            for key in keys:
                select_keys = "%s`%s`, " % (select_keys, key)
        sql = "select %s from `%s`" % (select_keys.rstrip(', '), table)
        return DBModel.sql_select_string(sql, where, limit, order, group)

    @staticmethod
    def sql_delete(table, where=None):
        sql = "delete from `%s`" % table
        if where != None and len(where) > 0:
            sql += " where %s" % where
        return sql

    # /**
    #  *
    #  *    组合查询条件  and   参数键值对数组  返回 拼接后字符串
    #  *    @where  map
    #  *    @conmap map 比较条件，默认为＝
    #  *    @return  string
    # **/
    @staticmethod
    def sql_and(where, conmap={}, keys=None, clearblank=False):
        condition = ''
        if keys != None:
            for key in keys:
                if where.has_key(key) and where[key] != None:
                    if clearblank == True and len(str(where[key])) == 0:
                        continue
                    condition = "%s`%s`%s'%s' and " % (
                    condition, key, conmap.get(key, '='), convert_2_string(where[key]))
        else:
            for key in where:
                if where[key] == None or (clearblank == True and len(str(where[key])) == 0):
                    continue
                condition = "%s`%s`%s'%s' and " % (condition, key, conmap.get(key, '='), convert_2_string(where[key]))
        return condition.rstrip(" and ")

    # /**
    #  *
    #  *    组合查询条件  or   参数键值对数组  返回 拼接后字符串
    #  *    @where  map
    #  *    @conmap map 比较条件，默认为＝
    #  *    @return  string
    # **/
    @staticmethod
    def sql_or(where, conmap={}, keys=None, clearblank=False):
        condition = ''
        if keys != None:
            for key in keys:
                if where.has_key(key) and where[key] != None:
                    if clearblank == True and len(str(where[key])) == 0:
                        continue
                    condition = "%s`%s`%s'%s' or " % (
                    condition, key, conmap.get(key, '='), convert_2_string(where[key]))
        else:
            for key in where:
                if where[key] == None or (clearblank == True and len(str(where[key])) == 0):
                    continue
                condition = "%s`%s`%s'%s' or " % (condition, key, conmap.get(key, '='), convert_2_string(where[key]))
        return condition.rstrip(" or ")

    def __init__(self, db_config, readonly=False):
        self.db_config = db_config
        self.readonly = readonly
        self.tansationstart = False
        self.connection = None
        self.lastresult = None

    def _connect_db(self):
        if self.connection == None:
            self.connection = pymysql.connect(
                host=self.readonly and DBModel.choose_mysql_host_s(self.db_config['host_s']) or self.db_config['host'],
                user=self.db_config['user'],
                passwd=self.db_config['passwd'],
                db=self.db_config['db'],
                port=int(self.db_config.get('port', 3306)),
                charset=self.db_config.get('charset', 'utf8'),
                cursorclass=self.db_config.get('cursorclass', pymysql.cursors.DictCursor),
            )

        return self.connection

    def _close_db(self, transation=False):
        if self.connection != None and self.tansationstart == transation:
            self.connection.close()
            self.connection = None

    def _commit_db(self, transation=False):
        if not self.readonly and self.connection != None and self.tansationstart == transation:
            self.connection.commit()

    def _rollback_db(self):
        if not self.readonly and self.connection != None:
            self.connection.rollback()

    # 执行多条sql语句
    def executemanay(self, sql, data, options=None, connected=False):
        try:
            if connected == False:
                self._connect_db()

            cursor = self.connection.cursor()
            if options != None:
                sqls = self._generate_sqls(sql, options)
                for sql in sqls:
                    cursor.executemany(sql, data)
                    self.lastresult = cursor
            else:
                cursor.executemany(sql, data)
                self.lastresult = cursor

            self._commit_db()
        except Exception, e:
            self.lastresult = None
            logger.error("executemanay sql failed sql=[%s],data=[%s],msg=[%s]:" % (repr(sql), repr(data), repr(e)))
        finally:
            if connected == False:
                self._close_db()

        return self.lastresult

    # 执行sql语句
    def execute(self, sql, options=None, connected=False):
        try:
            if connected == False:
                self._connect_db()

            cursor = self.connection.cursor()
            if options != None:
                sqls = self._generate_sqls(sql, options)
                for sql in sqls:
                    cursor.execute(sql)
                    self.lastresult = cursor
            else:
                cursor.execute(sql)
                self.lastresult = cursor

            self._commit_db()
        except Exception, e:
            self.lastresult = None
            logger.error("execute sql failed sql=[%s],msg=[%s]:" % (repr(sql), repr(e)))
        finally:
            if connected == False:
                self._close_db()

        return self.lastresult

    def GetCount(self, table, where=None, limit=None, order=None, group=None, options=None, connected=False):
        sql = "select count(*) as `total_count` from `%s`" % table
        sql = DBModel.sql_select_string(sql, where, limit, order, group)
        ret = self.GetList(sql, options=options, connected=connected)
        count = 0
        for item in ret:
            count += item['total_count']
        return count

    # # 返回查询资源结果集
    # def Query(self, sql, options=None):
    #     return self.execute(sql)

    # 获取单条数据
    def GetOne(self, sql, options=None, connected=False):
        result_one = {}
        try:
            sqls = self._generate_sqls(sql, options)
            if connected == False:
                self._connect_db()
            for sql in sqls:
                if self.execute(sql, connected=True) != None:
                    result_one = self.lastresult.fetchone()
                    if result_one and len(result_one) > 0:
                        break
        except Exception, e:
            logger.error("GetOne sql failed sql=[%s],msg=[%s]:" % (repr(sql), repr(e)))
        finally:
            if connected == False:
                self._close_db()
        if result_one == None:
            result_one = {}

        return result_one

    # 获取数据列表
    def GetList(self, sql, options=None, connected=False):
        result_list = []
        try:
            limit_count = options and options.get('limit_count')
            sqls = self._generate_sqls(sql, options)
            if connected == False:
                self._connect_db()
            for sql in sqls:
                if self.execute(sql, connected=True) != None:
                    result_list.extend(self.lastresult.fetchall())
                    if limit_count and len(result_list) >= limit_count:
                        # 有指定数量限制
                        result_list = result_list[:options['limit_count']]
                        break

            if options != None and options.has_key('group_by') and type(options['group_by']) == list:
                temp_result_list = []
                group_by_filter_map = {}
                for record in result_list:
                    group_by_key = ""
                    for key in options['group_by']:
                        group_by_key += record[key] + "_"
                    if group_by_filter_map.has_key(group_by_key):
                        continue
                    group_by_filter_map[group_by_key] = True
                    temp_result_list.append(record)
                result_list = temp_result_list
            if options != None and options.has_key('order_by') and type(options['order_by']) == list:
                # options['order_by'] = [{"key":"P","reverse":True},{"key":"GD","reverse":False}]
                # 从次要到主要的顺序来进行排序
                for item in options['order_by'][::-1]:
                    result_list.sort(key=lambda x: x[item['key']], reverse=item.get('reverse', False))
        except Exception, e:
            logger.error("GetList sql failed sql=[%s],msg=[%s]:" % (repr(sql), repr(e)))
        finally:
            if connected == False:
                self._close_db()

        return result_list

    # 获取分页数据
    # TODO:暂不支持多表操作
    def GetPage(self, sql, params={}):
        page = int(params.get('page', 1))
        num = int(params.get('num', 20))
        sql = sql.split('LIMIT')[0].split('limit')[0].strip()
        sql = '%s LIMIT %d,%d' % (sql, (page - 1) * num, num)
        return self.GetList(sql)

    # 返回上次执行Sql语句里影响的行数
    def affected_rows(self):
        if self.lastresult:
            return self.lastresult.rowcount
        return -1

    # 返回插入最后一次的ID
    def insert_id(self):
        if self.lastresult:
            return self.lastresult.lastrowid
        return -1

    # 开启事务
    def TransationStart(self):
        if self.readonly:
            return
        self._connect_db()
        self.tansationstart = True

    # 成功执行
    def TransationCommit(self, commit=True):
        if self.readonly:
            return
        if commit == True:
            self._commit_db(True)
        self._close_db(True)
        self.tansationstart = False

    # 回滚事务
    def TransationRollback(self):
        if self.readonly:
            return
        self._rollback_db()
        self._close_db(True)
        self.tansationstart = False

    def _generate_sqls(self, sql, options=None):
        if options == None or "##TABLE_INDEX##" not in sql:
            return [sql]

        if options.get('table_index') != None:
            return [sql.replace("##TABLE_INDEX##", str(options['table_index']))]
        elif options.get('table_count') != None:
            sqls = []
            if options.get('desc', True) == True:
                range_count = range(options['table_count'] - 1, -1, -1)
            else:
                range_count = range(0, options['table_count'])
            for table_index in range_count:
                sqls.append(sql.replace("##TABLE_INDEX##", str(table_index)))
            return sqls
        elif options.get('table_index_list') != None and type(options['table_index_list']) == list:
            sqls = []
            for index in range(0, len(options['table_index_list'])):
                table_index = options['table_index_list'][index]
                sqls.append(sql.replace("##TABLE_INDEX##", str(table_index)))
            return sqls
        else:
            return [sql]
