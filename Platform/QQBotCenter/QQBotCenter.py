# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from CONFIGS import *

from Libraries.Singleton.Singleton import Singleton
import QQBot
from HttpClient import HttpClient
from Libraries.mythreadpool import WorkerManager,Worker

def oneclickstart():
    # 只有top module的函数才能序列化（多进程调用的target）
    QQBot.main(mode='api')

@Singleton
class QQBotCenter(object):
    def __init__(self):
        self.HttpClient_Ist = HttpClient()

    def run(self,groups):
        print('QQBotcenter.py run',groups)
        QQBot.main(mode='api',groups=groups)
    def getQRUrlDelegate(self):
        return QQBot.getQRUrlDelegate(HttpClient_Ist=self.HttpClient_Ist)

    def continueLogin(self,*args,**kwargs):
        # wm = WorkerManager(2) # 创建线程池
        # wm.add_job(QQBot.loginWithDelegate,*args,**kwargs) # 将所有请求加入队列中
        # wm.start()
        # wm.wait_for_complete()
        # kwargs = wm.get_result()
        groups = args
        # QQBot.loginWithDelegate(
        #     *args,
        #     **kwargs
        # )
        from Platform.CeleryCenter import QQBot as qqbotCelery
        # 10s 后开始执行异步任务
        qqbotCelery.qqbot_bg.apply_async(target=QQBot.loginWithDelegate,args=[groups, kwargs], countdown=10)
        return
        # wm.add_job(qqBotCenter.continueLogin,groups,kwargs)
        # wm.start()
        # t = threading.Thread(target=qqBotCenter.continueLogin, args=(groups,kwargs))
        # t.setDaemon(True)
        # t.start()#不能join，join就堵塞了，无法返回

        # 多进程： windows上开不起来？？？
        # p = multiprocessing.Process(target=qqBotCenter.continueLogin, args=(groups,kwargs))
        # p.start()
        # p.join()

        # kwargs = None
        # pool = multiprocessing.Pool()
        # result = Queue.Queue()
        #
        # '''
        # 将子进程对象存入队列中。
        # '''
        # q.put(pool.apply_async(qqBotCenter.getQRUrlDelegate, args=()))  # 维持执行的进程总数为10，当一个进程执行完后添加新进程.
        # '''
        # 因为这里使用的为pool.apply_async异步方法，因此子进程执行的过程中，父进程会执行while，获取返回值并校验。
        # '''
        # while True:
        #     kwargs = result.get().get()
        #     if kwargs:
        #         pool.terminate()  # 结束进程池中的所有子进程。
        #         break
