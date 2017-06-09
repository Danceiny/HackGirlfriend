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
from collections import defaultdict,Counter
import Libraries.Utils as utils
import numpy as np

import matplotlib.pyplot as plt

import QQChatCenter as center


# time part
# 统计聊天频率
def split_time_str(str_time):
    return re.split('[- :]',str_time)

def get_time_dict(str_time):
    tu_time_key = ('year','month','day','hour','minute','second')
    struct_time = time.strptime(str_time,'%Y-%m-%d %H:%M:%S')
    tu_time_value = tuple(struct_time)[:-1]
    return dict((name, value) for name, value in zip(tu_time_key, tu_time_value))
    # get_time_dict('2017-02-12 12:31:00')

def qq_strptime(str_time):
    return time.strptime(str_time,'%Y-%m-%d %H:%M:%S')

def get_hour_stats(records, debug=False):
    hourArray = []
    for userInfo in records:
        # hourArray.append(get_time_dict(userInfo.get('str_time')).get('hour'))
        hourArray.append(qq_strptime(userInfo.get('str_time')).tm_hour)

    if debug:print(len(hourArray))
    hour_counts = Counter(hourArray)
    # 对数据进行排序
    return hourArray,sorted(hour_counts.items())

def get_weekday_stats(records, debug=False):
    weekdayArray = []
    for userInfo in records:
        weekdayArray.append(qq_strptime(userInfo.get('str_time')).tm_wday)
    if debug:print(len(weekdayArray))
    weekday_counts = Counter(weekdayArray)
    # 对数据进行排序
    return weekdayArray,sorted(weekday_counts.items())

def hourProcess(records,debug=False):
    hourArray,sortByHour = get_hour_stats(records)
    postMessageLabel = []
    postMessageNum = []
    for key, value in sortByHour:
        postMessageLabel.append(key)
        postMessageNum.append(value)
    plotSimpleStats(postMessageLabel,postMessageNum,'hour')

def plotSimpleStats(timeArray,postMessageLabel,postMessageNum,type=''):
    # 生成发贴柱状图
    N = len(postMessageNum)

    ind = np.arange(N) + 0.5  # the x locations for the groups
    # print(ind) #x轴上的数值
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects = ax.bar(ind, postMessageNum, width, color='r')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('message number')
    ax.set_title('QQ message number of '+type+',total message ( ' + str(len(timeArray)) + ")")
    ax.set_xticks(ind + width)
    ax.set_xticklabels(postMessageLabel)

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., height, '%d' % int(height), ha='center', va='bottom')
    autolabel(rects)
    plt.show()

def weekdayProcess(records,debug=False):
    weekdayArray,sortByWeekday = get_weekday_stats(records)
    postMessageLabel = []
    postMessageNum = []
    for key,value in sortByWeekday:
        postMessageLabel.append(key)
        postMessageNum.append(value)
    plotSimpleStats(weekdayArray,postMessageLabel,postMessageNum,'weekday')

records =center.get_records_from_json_file(center.FILE_JSON_RECORDS)
weekdayProcess(records)