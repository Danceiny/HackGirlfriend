# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from CONFIGS import *

from Libraries.Singleton.Singleton import Singleton
import QQBot
from HttpClient import HttpClient
from Libraries.mythreadpool import WorkerManager,Worker
import threading
import os
from Libraries.Utils import concat_dirs,get_now_time_str_ms
import traceback
from QMessage import QMessage
from Login import Login
def oneclickstart():
    # 只有top module的函数才能序列化（多进程调用的target）
    QQBot.main(mode='api')
###########   part   #####################
def deleteAllQRCode(path):
    if os.path.isfile(path) and path.endswith(('png','jpg','gif')):
        os.remove(os.path.abspath(path))
    elif os.path.isdir(path):
        for img in os.listdir(os.path.abspath(path)):
            if os.path.isfile(img) and img.endswith(('png','jpg','gif')):
                os.remove(os.path.join(path,img))
@Singleton
class QQBotCenter(object):
    def __init__(self):
        self.HttpClient_Ist = HttpClient()

    def run(self,groups):
        print('QQBotcenter.py run',groups)
        QQBot.main(mode='api',groups=groups)

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
        if kwargs.get('mode') == 'celery':
            from Platform.CeleryCenter.QQBot import celery as qqbotCelery
            # 10s 后开始执行异步任务
            qqbotCelery.qqbot_bg.apply_async(target=QQBot.loginWithDelegate,args=[groups, kwargs], countdown=10)
        else:
            # wm = WorkerManager(2)  # 创建线程池
            # wm.add_job(QQBot.loginWithDelegate,*groups,**kwargs)
            # wm.start()
            t = threading.Thread(target=QQBot.loginWithDelegate,args=groups,kwargs=kwargs)
            t.setDaemon(True)
            t.start()#不能join，join就堵塞了，无法返回
        return

    def getQRUrlDelegate(self,own_qq_number=0):

        # do:
        # 1. prelogin,
        # 2. download qrcode img and return and local download abs path.
        # 3. return loginDelegate(Login() class instance), url(img abs path)
        HttpClient_Ist = HttpClient()
        try:
            cur_file_path = os.getcwd()
            if not cur_file_path.endswith('Applications'):
                cur_file_path = concat_dirs(True, cur_file_path,
                                            'Applications')
            abs_vpath = concat_dirs(True, cur_file_path, 'QQBot', 'static',
                                    'images', '{}.png'.format(
                    get_now_time_str_ms().replace('.', '')))
            loginParams = {'DELETE_PIC': True,
                           'VPATH': VPATH if abs_vpath == '' else abs_vpath}
            qqLoginDelegate = Login(own_qq_number, loginParams)
            qqLoginDelegate.preLogin()
            url = qqLoginDelegate.getQRCodeUrl(Try=5)
            return {'loginDelegate': qqLoginDelegate, 'url': url,
                    'httpClientIst': HttpClient_Ist}
        except Exception, e:
            logger.error(str(e))
            traceback.print_exc()
            deleteAllQRCode(
                concat_dirs(True,__file__,'..','..','..','Applications',\
                                                         'QQBot','static','images'))
            os._exit(-1)

    def loginWithDelegate(self,*args, **kwargs):
        qqLoginDelegate = None
        HttpClient_Ist = None
        groups = args
        print groups, kwargs, 'b'
        for k, v in kwargs.items():
            if 'loginDelegate' == k:
                qqLoginDelegate = v
            elif 'httpClientIst' == k:
                HttpClient_Ist = v
            elif 'loginParams' == k:
                loginParams = v

        if qqLoginDelegate != None:
            qqLoginDelegate.login()
            qMsg_Ist = QMessage(HttpClient_Ist, qqLoginDelegate)

            qMsg_Ist.setDaemon(True)
            qMsg_Ist.start()

            # 把所有群加进t_check实例的GroupNameList，GroupCodeList列表中
            qMsg_Ist.watch_group()

            try:
                for group in groups:
                    tmp = group.strip('\n').strip('\r').strip()
                    if str(tmp) in qMsg_Ist.GroupNameList:
                        qMsg_Ist.GroupWatchList.append(
                            str(qMsg_Ist.GroupNameList[str(tmp)]))
                        logger.info("关注:" + str(tmp))

                    else:
                        logger.error("无法找到群：" + str(tmp))
            except Exception, e:
                logger.error("读取组存档出错:" + str(e))
            qMsg_Ist.join()
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
