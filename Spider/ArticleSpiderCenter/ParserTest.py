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
import re
import random
from Configs import *
import re
############## data normalization ##############

from Utils import *
from Parser import *

from Libraries.Utils import *


kexuewangURL = 'http://blog.sciencenet.cn/blog-57081-950915.html'
if __name__ == '__main__':


    filename = getHostnameOfUrl(kexuewangURL).replace('.','_') + '_template.html'
    print filename
    # tree = save_tree(kexuewangURL,filename)

    tree = resume_tree(filename)
    kexuewangParser = KexuewangBlogParser(tree=tree,url_example='http://blog.sciencenet.cn/blog-57081-950915.html')
    print kexuewangParser.parse_news_content(tree)

