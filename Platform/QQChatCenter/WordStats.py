# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import jieba
import codecs
import json
from collections import defaultdict
import Libraries.Utils as utils
import jieba.analyse
from optparse import OptionParser
FILE_JSON_RECORDS = u'json汪睿(1458110685).txt'

READ_CACHE_LINES = 10000


def get_extracted_tags(content, topK, type='list',sep=','):
    # return eval('get_extracted_tags_' + type)(content, topK)
    if type=='list':
        return get_extracted_tags_list(content, topK)
    elif type=='str':
        return get_extracted_tags_str(content,topK,sep)

def get_extracted_tags_list(content, topK):
    return jieba.analyse.extract_tags(content, topK)

def get_extracted_tags_str(content,topK,sep):
    return sep.join(jieba.analyse.extract_tags(content,topK))

def get_seg_list(content,cut_all=False):
    return jieba.cut(content,cut_all)

with codecs.open(FILE_JSON_RECORDS, 'rb','utf-8') as f:
    lines = f.readlines()
    if not lines:
        print 'blank'
    i = 0
    seg_list = []
    lastline = None
    sentences = ''
    for line in lines:
        record = json.loads(line.encode('utf-8'))
        sentence = record['sentence'].encode('utf-8')
        # 分词
        seg_list.extend(jieba.cut(sentence,cut_all=False))

        sentences += sentence + '\n'

    # 提取关键字
    # tags = jieba.analyse.extract_tags(sentences, topK=100)
    # print(",".join(tags))

    tags = get_extracted_tags(sentences,5)
    print(",".join(tags))

