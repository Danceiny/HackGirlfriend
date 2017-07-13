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
