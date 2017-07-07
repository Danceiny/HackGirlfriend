#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'Danceiny'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import codecs
import requests
import urllib,urllib2
import pickle
import pickletools
import requests
from lxml import etree
import time

def write_sqls_2_txt(sqls,outfile):
    with codecs.open(outfile, 'w', 'utf-8') as f:
        if type(sqls) == list:
            for sql in sqls:
                print sql
                f.write(sql + '\n')
        elif type(sqls) == str or type(sqls) == unicode:
            f.write(sqls+'\n')
        else:
            print '不支持的类型！'

def generate_insert_news_sql(values, items=None,base_sql=''):
    # items = {'a_id': '', 'category': '','title':'', 'content': '', 'show_time': 0, 'hits': 0}
    #
    # base_sql = "insert `cecc`.`t_cc_news_0`(`a_id`,`category`,`title`,`content`,`show_time`,`hits`) values('%s','%s','%s','%s',%d,%d)"

    # items['a_id'] = str(int(values[0])).decode("UTF-8")
    # items['title'] = values[1].decode("UTF-8")
    # items['category'] = values[2].decode("UTF-8")
    # items['content'] = values[3].decode("UTF-8")
    # items['show_time'] = int(values[4])
    # items['hits'] = int(values[5])

    sql = base_sql % (items.values())
    return sql