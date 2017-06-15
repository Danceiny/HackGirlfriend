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