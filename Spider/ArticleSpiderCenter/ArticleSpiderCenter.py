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
RAND_RANGE = (1000,10000)

import random
from Configs import *
############## data normalization ##############


from Parser import *

if __name__ == '__main__':
    articleType =








#############       IO       ###############


def generate_insert_news_sql(values, items=None):
    if items == None: items = {'a_id': '', 'category': '','title':'', 'content': '', 'show_time': 0, 'hits': 0}

    BASE_SQL = "insert `cecc`.`t_cc_news_0`(`a_id`,`category`,`title`,`content`,`show_time`,`hits`) values('%s','%s','%s','%s',%d,%d)"

    items['a_id'] = str(int(values[0])).decode("UTF-8")
    items['title'] = values[1].decode("UTF-8")
    items['category'] = values[2].decode("UTF-8")
    items['content'] = values[3].decode("UTF-8")
    items['show_time'] = int(values[4])
    items['hits'] = int(values[5])

    sql = BASE_SQL % (items['a_id'], items['category'], items['title'],
                      items['content'], items['show_time'], items['hits'])
    return sql



