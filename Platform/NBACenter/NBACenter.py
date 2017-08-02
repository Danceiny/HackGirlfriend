# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


from Libraries.Singleton.Singleton import Singleton
from Libraries.mythreadpool import WorkerManager,Worker
import threading
import os
from Libraries.Utils import concat_dirs,get_now_time_str_ms,get_now_time_int
import Libraries.ErrorDefine as ED
import traceback

import sys
import csv
import urllib2
import requests
import re
from itertools import izip
from lxml import html, etree
from bs4 import BeautifulSoup
from bs4.element import Comment
from datetime import datetime
import time
import json
from Libraries.Singleton.Singleton import Singleton

from Libraries.DBModel import *
from Platform.ConfigCenter.ConfigCenter import ConfigCenter
from Platform.LogCenter.LogCenter import LogCenter
from Libraries.Utils import *

db_model = DBModelFactory.instance().get_db_model()
# self.db_model_read = DBModelFactory.instance().get_db_model(readonly=True)

# self.table_name_user = self.conf.get('RDS', 'table_name_zuiwan_user')
# self.table_name_user_count = self.conf.getint('RDS', 'table_name_zuiwan_user_count')
# self.table_name_user_keys = json.loads(self.conf.get('RDS', 'table_name_zuiwan_user_keys'))
table_name_user = "zuiwan_user"
table_name_user_count = 1
table_name_user_keys = (
'zuser_id', 'nick_name', 'email', 'create_time', 'avatar_url', 'credits', 'role', 'psw', 'real_name', 'sex')

table_name_meeting = "zuiwan_meeting"
table_name_meeting_count = 1
table_name_meeting_keys = ('meeting_id', 'topic', 'start_time', 'duration', 'des', 'people')
from SubstitutionPatterns import *
from Libraries.Celery import celery

@Singleton
class NBACenter(object):
    def __init__(self):
        self.logger = LogCenter.instance().get_logger('NBACenterLog')
        self.db_model = DBModelFactory.instance().get_db_model()
        self.table_name = "nba"
        self.table_name_count = 1
        self.table_name_keys = ('id', 'operation', 'des', 'time','user_ip')


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}

@celery.task(bind=True,
    default_retry_delay=300,
    max_retries=5)
def celery_substitution_patterns(centerIst=None):
    start_time = time.time()
    nba_substitution_crawler()
    print("--- %s seconds ---" % (time.time() - start_time))
    return start_time

# bind = true
# 这个参数告诉 Celery 发送一个 self 参数到我的函数，我能够使用它(self)来记录状态更新。
@celery.task()
def long_time_def():
    i = 0
    while i < 100:
        i+= 1
        time.sleep(0.2)
    return 'finished'


@celery.task(bind = True)
def updating_long_time_def(self):
    i = 0
    while i < 100:
        i+= 1
        self.update_state(state='PROGRESS',meta={'i':i})
        time.sleep(0.2)
    return 'finished'
@celery.task()
def writeDBTest(self,data=None):
    '''
    :param data {}
    :return:
    '''
    if data == None:
        data = {'nick_name':'nbatestcelery','psw':'none'}
    result = {'code': ED.no_err}
    if not 'zuser_id' in data or len(data.get('zuser_id','')) <= 0:
        data['zuser_id'] = get_now_time_str_ms().replace('.', '')  # like '1497257116332'
    if not 'create_time' in data or data.get('create_time',0) == 0:
        data['create_time'] = get_now_time_int()
    else:
        return {'code':ED.err_params}
    sql = db_model.sql_insert(table=table_name_user, data=data, keys=table_name_user_keys)
    flag = db_model.execute(sql)
    if flag == None or flag.rowcount <= 0:
        result['code'] = ED.unknown_err
    return result