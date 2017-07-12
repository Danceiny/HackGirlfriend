# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import current_app
from Libraries.Celery import make_celery
celery = make_celery(current_app)
@celery.task()
def qqbot_bg(*args,**kwargs):
    # QQ聊天机器人守护进程/线程
    print('QQ聊天机器人守护进程/线程',args,kwargs)
    pass

@celery.task()
def save_chat_record():
    # 私聊 && 群聊 && {登录者：关注群}
    # redis缓存，MongoDB持久化
    pass
