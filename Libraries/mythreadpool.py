#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import Queue,sys,threading
import urllib2,os

class Worker(threading.Thread):
    def __init__(self,workQueue,resultQueue,**kwargs):
        threading.Thread.__init__(self,**kwargs)
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue

    def run(self):
        while True:
            try:
                callable, args, kwargs = self.workQueue.get(False)#从队列中取出一个任务
                res = callable(*args,**kwargs)
                self.resultQueue.put(res)   #存放处理结果到队列中
            except Queue.Empty:
                break

class WorkerManager:
    '''
    线程池管理器
    '''
    def __init__(self,num_of_workers=10):
        self.workQueue = Queue.Queue()  #请求队列
        self.resultQueue = Queue.Queue()    #输出结果的队列
        self.workers = []
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self,num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue,self.resultQueue)#创建工作线程
            self.workers.append(worker) #加入线程队列中
    def start(self):    #启动线程
        for w in self.workers:
            w.start()
    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop() #从池中取出一个线程处理请求
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker) #重新加入线程池中
        print('All jobs were completed.')

    def add_job(self,callable,*args,**kwargs):
        self.workQueue.put((callable,args,kwargs))
    def get_result(self,*args,**kwargs):
        return self.resultQueue.get(*args,**kwargs)



# pip install threadpool

def download_file(url):
    print("Begin download {}".format(url))
    urlhandler = urllib2.urlopen(url)
    fname = os.path.basename(url) + ".html"
    with open(fname,"wb") as f:
        while True:
            chunk = urlhandler.read(1024)
            if not chunk:
                break
            f.write(chunk)

def test_mythreadpool():
    urls = ["http://wiki.python.org/moni/WebProgramming",
           "https://www.createspace.com/3611970",
           "http://wiki.python.org/moin/Documention"]
    wm = WorkerManager(2) # 创建线程池
    for i in urls:
        wm.add_job(download_file, i) # 将所有请求加入队列中
    wm.start()
    wm.wait_for_complete()

def test_threadpool():
    import urllib2
    import os
    import time
    import threadpool
    urls = ["http://wiki.python.org/moni/WebProgramming",
            "https://www.createspace.com/3611970",
            "http://wiki.python.org/moin/Documention"]
    pool_size = 2
    pool = threadpool.ThreadPool(
        pool_size)  # 创建线程池，大小为 2
    requests = threadpool.makrRequests(download_file, urls)
    # 创建工作请求
    [pool.putRequest(req) for req in requests]
    print("putting request to pool")
    pool.putRequest(threadpool.WorkRequest(download_file, args=[
        "http://chrisarndt.de/proj ects/threadpool/api/", ]))
    # 将具体的请求放入线程池
    pool.putRequest(threadpool.WorkRequest(download_file, args=["https://pypi.python.org/p ypi/threadpool",]))
    pool.poll()  # 处理任务队列中的新的请求
    pool.wait()
    print("destory all threads before exist")
    pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出