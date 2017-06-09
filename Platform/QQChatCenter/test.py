# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from ctypes import *
import time
import os
import codecs
import re
import json
from collections import defaultdict
import Libraries.Utils as utils

FILE_TO_READ = u'json汪睿(1458110685).txt'
FILE_JSON_RECORDS = u'json' + FILE_TO_READ
READ_CACHE_LINES = 10000
with codecs.open(FILE_TO_READ, 'r','utf-8') as f:
    lines = f.readlines()
    if not lines:
        print 'blank'
    i = 0
    lastline = None
    for line in lines:
        record = json.loads(line.encode('utf-8'))
        print record