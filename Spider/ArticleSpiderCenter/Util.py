#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'Danceiny'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import codecs
import requests
import urllib, urllib2
import pickle
import pickletools
import requests
from lxml import etree
import time


def grab_tree(url,timeout=1):
    while timeout:
        r = requests.get(url)
        if r.text != None:
            return etree.HTML(r.text)
        timeout -= 1

def save_tree(url,filename,encoding='utf-8'):
    r = requests.get(url)
    # r.text is unicode
    with codecs.open(filename, 'w', encoding) as f:
        pickle.dump(r.text, f)#, protocol=2


def save_trees(urls):
    for url in urls:
        save_tree(url)

def resume_tree(filename,encoding='utf-8'):
    with codecs.open(filename, 'r',encoding) as f:
        return etree.HTML(pickle.loads(f.read()))

def resume_trees(filenames,encoding='utf-8'):
    for filename in filenames:
        with codecs.open(filename, 'r',encoding) as f:
            return etree.HTML(pickle.loads(f.read()))