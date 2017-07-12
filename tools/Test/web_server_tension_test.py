# -*- coding: utf-8 -*-
__author__ = 'klb3713'  #https://gist.githubusercontent.com/klb3713/6077267/raw/236aa367075262ef776e66499313d891a629b482/web_test.py


import threading, time, httplib
from Libraries.Utils import get_now_time_str_ms
HOST = "118.89.27.96" #主机地址 例如192.168.1.101
PORT = 80 #端口

HOST = '192.168.136.2'
PORT = 8098
TOTAL = 0 #总数
SUCC = 0 #响应成功数
FAIL = 0 #响应失败数
EXCEPT = 0 #响应异常数
MAXTIME=0 #最大响应时间
MINTIME=100 #最小响应时间，初始值为100秒
TOTALTIME = 0 #总的响应时间
GT3=0 #统计3秒内响应的
LT3=0 #统计大于3秒响应的

# 创建一个 threading.Thread 的派生类
class RequestThread(threading.Thread):
    # 构造函数
    def __init__(self, thread_name, post_data,uri,method='POST'):
        threading.Thread.__init__(self)
        self.test_count = 0
        self.post_data = post_data
        self.URI = uri
        self.method = method

    # 线程运行的入口函数
    def run(self):

        self.test_performace()


    def test_performace(self):
        global TOTAL
        global SUCC
        global FAIL
        global EXCEPT
        global GT3
        global LT3
        global TOTALTIME
        try:
            st = time.time()
            conn = httplib.HTTPConnection(HOST, PORT, False)
            if self.method == 'GET':
                self.URI += self.post_data
                # print(''.join(('---------------------------------------------',self.URI,'-----------------------------')))
            conn.request(self.method, self.URI, self.post_data,headers={"Content-Type":"application/json"})
            res = conn.getresponse()
            # print 'version:', res.version
            # print 'reason:', res.reason
            # print 'status:', res.status
            # print 'msg:', res.msg
            # print 'headers:', res.getheaders()
            # print  'read',res.read()
            time_span = time.time()-st
            #print '%s:%f\n'%(self.name,time_span)
            if res.status == 200:
                TOTAL+=1
                SUCC+=1
                TOTALTIME += time_span
            else:
                TOTAL+=1
                FAIL+=1

            self.maxtime(time_span)
            self.mintime(time_span)
            if time_span>3:
                GT3+=1
            else:
                LT3+=1
        except Exception,e:
            print e
            TOTAL+=1
            EXCEPT+=1
        conn.close()

    def maxtime(self,ts):
        global MAXTIME
        if ts>MAXTIME:
            MAXTIME=ts
    def mintime(self,ts):
        global MINTIME
        if ts<MINTIME:
            MINTIME=ts

def post_test(thread_count, post_data):
    global TOTAL
    global SUCC
    global FAIL
    global EXCEPT
    global GT3
    global LT3
    global TOTALTIME
    global MINTIME
    global MAXTIME

    TOTAL = 0
    SUCC = 0
    FAIL = 0
    EXCEPT = 0
    MAXTIME=0
    MINTIME=100
    TOTALTIME = 0
    GT3=0
    LT3=0

    # main 代码开始
    print '===========task start==========='
    # 开始的时间
    start_time = time.time()
    # 并发的线程数
    #thread_count = 10

    i = 0
    TOTAL = 0
    while i < thread_count:
        # t = RequestThread("thread" + str(i), post_data,"/api/v1/zuiwan/user/modify")
        t = RequestThread("thread" + str(i), post_data,"/api/v1")
        t.start()
        i += 1

    t=0
    #并发数所有都完成或大于60秒就结束
    while TOTAL<thread_count and t<60:
        #print "total:%d,succ:%d,fail:%d,except:%d\n"%(TOTAL,SUCC,FAIL,EXCEPT)
        #print HOST,URI
        t+=1
        time.sleep(1)

    print '===========task end==========='
    print "thread_count: ", thread_count
    print "post_data: ", post_data
    print "total:%d,succ:%d,fail:%d,except:%d"%(TOTAL,SUCC,FAIL,EXCEPT)
    print 'response maxtime:',MAXTIME
    print 'response mintime',MINTIME
    print 'great than 3 seconds:%d,percent:%0.2f'%(GT3,float(GT3)/TOTAL)
    print 'less than 3 seconds:%d,percent:%0.2f'%(LT3,float(LT3)/TOTAL)
    if SUCC != 0:print 'average time: %0.2f'%(TOTALTIME/SUCC)

def get_test(thread_count, post_data):
    global TOTAL
    global SUCC
    global FAIL
    global EXCEPT
    global GT3
    global LT3
    global TOTALTIME
    global MINTIME
    global MAXTIME

    TOTAL = 0
    SUCC = 0
    FAIL = 0
    EXCEPT = 0
    MAXTIME=0
    MINTIME=100
    TOTALTIME = 0
    GT3=0
    LT3=0

    # main 代码开始
    print '===========task start==========='
    # 开始的时间
    start_time = time.time()
    # 并发的线程数
    #thread_count = 10

    i = 0
    TOTAL = 0
    while i < thread_count:
        # t = RequestThread("thread" + str(i), post_data,"/api/v1/zuiwan/user/modify")
        t = RequestThread("thread" + str(i), post_data,"/api/v1",method='GET')
        t.start()
        i += 1

    t=0
    #并发数所有都完成或大于60秒就结束
    while TOTAL<thread_count and t<60:
        #print "total:%d,succ:%d,fail:%d,except:%d\n"%(TOTAL,SUCC,FAIL,EXCEPT)
        #print HOST,URI
        t+=1
        time.sleep(1)

    print '===========task end==========='
    print "thread_count: ", thread_count
    print "post_data: ", post_data
    print "total:%d,succ:%d,fail:%d,except:%d"%(TOTAL,SUCC,FAIL,EXCEPT)
    print 'response maxtime:',MAXTIME
    print 'response mintime',MINTIME
    print 'great than 3 seconds:%d,percent:%0.2f'%(GT3,float(GT3)/TOTAL)
    print 'less than 3 seconds:%d,percent:%0.2f'%(LT3,float(LT3)/TOTAL)
    print 'average time: %0.2f'%(TOTALTIME/SUCC)

def singleTest():
    conn = httplib.HTTPConnection(HOST, PORT, False)
    conn.request('POST', "/api/v1/zuiwan/user/modify",
                 '{"request-body":{"getVideoUrl":{"videoType":"sohu_url","videoId":"http://tv.sohu.com/20130526/n377096321.shtml"}}}')
    res = conn.getresponse()
    if res.status == 200:
        print "request ok"
    else:
        print "request fail! status: ", res.status


if __name__ == "__main__":
    post_datas = ['{"action":"add","zuser_id":"%s","psw":"password","user_name":"http://tv.sohu.com/20130526/n377096321.shtml"}' % (get_now_time_str_ms().replace('.','')),
                  '{"action":"update","zuser_id":"%s","psw":"password","nick_name":"http://tv.sohu.com/20130526/n377096321.shtml"}'%(get_now_time_str_ms().replace('.','')),
                  '{"action":"add","zuser_id":"%s","psw":"password","user_name":"http://tv.sohu.com/20130526/n377096321.shtml"}'%(get_now_time_str_ms().replace('.','')),
                  '{"action":"delete","zuser_id":"%s","psw":"password","nick_name":"http://tv.sohu.com/20130526/n377096321.shtml"}'%(get_now_time_str_ms().replace('.',''))]

    get_params = ['/zuiwan/get-users-list','/zuiwan/get-user-detail?zuser_id=100']

    post_test(10, post_datas[0])
    post_test(20, post_datas[1])
    post_test(50, post_datas[2])
    post_test(10, post_datas[2])
    post_test(20, post_datas[2])
    get_test(50, get_params[0])
    get_test(20, get_params[1])
    get_test(50, get_params[0])
    get_test(50, get_params[1])

    #singleTest()