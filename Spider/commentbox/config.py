import os

MONGODB_DB = 'music'
# MONGODB_HOST = 'localhost'
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
PROXIES = []

REDIS_DB = 0
# REDIS_HOST = 'localhost'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DB = os.path.join(HERE, 'data/fake_useragent.json')

DEBUG = False

try:
    from local_settings import *  # noqa
except ImportError:
    pass
