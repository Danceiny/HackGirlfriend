# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from ConfigParser import ConfigParser
from celery import Celery
def make_celery(app):
    config_app_celery(app)
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

def config_app_celery(app):
    conf = ConfigParser()
    conf_name = os.path.join('PackageData', 'celery.conf')
    conf_path = os.path.dirname(os.path.dirname(__file__))
    conf.read(os.path.join(conf_path, conf_name))

    # app.config.update(
    #     CELERY_BROKER_URL='redis://localhost:6379',
    #     CELERY_RESULT_BACKEND='redis://localhost:6379'
    #     )
    app.config.update(
        CELERY_BROKER_URL=conf.get('DEFAULT','CELERY_BROKER_URL'),
        CELERY_RESULT_BACKEND=conf.get('DEFAULT','CELERY_RESULT_BACKEND')
        )
