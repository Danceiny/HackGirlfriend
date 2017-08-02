from flask import Flask
from flask_celery import Celery

app = Flask('celery_test')
app.config['CELERY_BROKER_URL'] = 'redis://localhost'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost'
celery = Celery(app)

@celery.task()
def add_together(a, b):
    return a + b

if __name__ == '__main__':
    result = add_together.delay(23, 42)
    print(result.get())


# Single-instance example from https://github.com/Robpol86/Flask-Celery-Helper
# example.py
import time
from flask import Flask
from flask_celery import Celery, single_instance
from flask_redis import Redis

app = Flask('example')
app.config['REDIS_URL'] = 'redis://localhost'
app.config['CELERY_BROKER_URL'] = 'redis://localhost'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost'
celery = Celery(app)
Redis(app)

@celery.task(bind=True)
@single_instance
def sleep_one_second(a, b):
    time.sleep(1)
    return a + b

if __name__ == '__main__':
    task1 = sleep_one_second.delay(23, 42)
    time.sleep(0.1)
    task2 = sleep_one_second.delay(20, 40)
    results1 = task1.get(propagate=False)
    results2 = task2.get(propagate=False)
    print(results1)  # 65
    if isinstance(results2, Exception) and str(results2) == 'Failed to acquire lock.':
        print('Another instance is already running.')
    else:
        print(results2)  # Should not happen.