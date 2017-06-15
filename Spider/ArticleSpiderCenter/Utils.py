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

def save_tree(url,filename):
    r = requests.get(url)
    f = open(filename, 'wb')
    pickle.dump(r.text, f, protocol=2)
    f.close()

def save_trees(urls):
    for url in urls:
        save_tree(url)

def resume_tree(filename):
    with codecs.open(filename, 'rb') as f:
        return etree.HTML(pickle.loads(f.read()))

def resume_trees(filenames):
    for filename in filenames:
        with codecs.open(filename, 'rb') as f:
            return etree.HTML(pickle.loads(f.read()))