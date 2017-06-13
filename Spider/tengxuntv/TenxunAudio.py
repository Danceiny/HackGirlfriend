# coding=utf-8
'''
使用说明：
流程：
    1，调用 getAudio() 得到搜索结果，其中参数 search_data为搜索内容, watch_count为观看次数下限
    2，调用writeToFile() 将结果整理到 result.txt当中
关于去重：
    将每次采用的视频的id写入ids.txt,则会在搜索结果中去掉这些已使用过的id
'''

import urllib2
import urllib
import json
import codecs

class TenxunAudio():
    def __init__(self):
        self.result_list = None
        self.ids = None

    def getAudio(self, search_data="test",watch_count=0):
        url = "http://s.video.qq.com/search"
        get_data = {
            "comment": "0",
            "num": "30",
            "otype": "json",
            "plat": "2",
            "pltimefilter": "1", # 时间长度
            "pubtime": "0", # 发布时间
            "query": search_data,
            "query_type": "0", # 分类
            "referrer": "http://v.qq.com/search.html?pagetype=3&ms_key=test&stj2=search.search&stag=txt.result",
            "sort":"0", # 排序
            "start": "0", # 起始
        }
        get_data = urllib.urlencode(get_data)
        response = urllib2.urlopen(url=url+"?"+get_data).read()
        if 'Json=' in response:
            response = response[response.index('Json=')+5:-1]
            response = json.loads(response)
            response = response.get('list')
        else:
            response = []

        result_list = []
        for one in response:
            if one.get("VA") < watch_count: # 观看次数小于100
                continue
            else:
                if not self.remove_the_repeats(id=one.get("ID")):
                    continue
                one_dict = {
                    "id":one.get("ID").encode("utf-8"),
                    "title":one.get("title").encode("utf-8"),
                    "watch_count":one.get("VA"),
                    "time":one.get("AT").encode("utf-8"),
                    "type":one.get("AQ").encode("utf-8"), # 清晰度
                    "url":("http://static.video.qq.com/TPout.swf?vid=%s&auto=0" % one.get('ID')).encode("utf-8")
                }
                result_list.append(one_dict)

        def key(one):
            return one.get('watch_count')

        result_list.sort(key=key,reverse=True)
        print "total_count:",len(result_list)
        self.result_list = result_list
        return result_list

    def writeToFile(self,filename="result.txt"):
        if self.result_list == None or len(self.result_list) <= 0:
            return False
        file = codecs.open(filename=filename,mode='w')
        for one in self.result_list:
            line = "时间："+one.get('time')+" 观看次数："+str(one.get('watch_count'))+" ID:"+one.get("id")+" 题目："+one.get('title')+" URL："+one.get('url')+"\n"
            file.write(line)
        file.flush()
        file.close()
    def remove_the_repeats(self,id):
        if self.ids == None:
            file = codecs.open("ids.txt")
            self.ids = file.readlines()
        for one in self.ids:
            for i,char in enumerate(one): # 去掉后面的 \r \n等字符
                if char in ("\r","\n"):
                    one = one[:i]
            if str(id) == one:
                return False
        return True

if __name__ == "__main__":
    tenxunAudio = TenxunAudio()
    response = tenxunAudio.getAudio(search_data="每日爆笑短片",watch_count=30)
    tenxunAudio.writeToFile()
    print "the end"
