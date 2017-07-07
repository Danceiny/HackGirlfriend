#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'Danceiny'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os
import codecs
import requests
import urllib, urllib2
import pickle
import pickletools
import requests
from lxml import etree
import time

RAND_RANGE = (1000, 10000)
import re
import random
from Configs import *
import re
############## data normalization ##############

from Util import *
from Parser import *

from Libraries.Utils import getHostnameOfUrl


def kexuewangTest():
    kexuewangURL = 'http://blog.sciencenet.cn/blog-57081-950915.html'
    filename = getHostnameOfUrl(kexuewangURL).replace('.', '_') + '_template.html'
    print filename
    # tree = save_tree(kexuewangURL,filename)

    tree = resume_tree(filename)
    kexuewangParser = KexuewangBlogParser(tree=tree, url_example='http://blog.sciencenet.cn/blog-57081-950915.html')
    print kexuewangParser.parse_blog_content(tree)


def hupuPostTest():
    hupuPostUrl = 'https://bbs.hupu.com/19453374.html'
    filename = getHostnameOfUrl(hupuPostUrl).replace('.', '_') + '_templage.html'
    # tree = save_tree(hupuPostUrl,filename)
    # tree = resume_tree(filename)
    tree = grab_tree(hupuPostUrl)
    hupuPostParser = HupuPostParser()
    hupuPostParser.parse_post_content(tree)


if __name__ == '__main__':
    hupuPostTest()