# -*- coding: utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))#把HackGirlfriend目录加载到$PYTHONPATH中

from flask import Flask
from flask_gzip import Gzip
from werkzeug.routing import BaseConverter
from flask_socketio import SocketIO
from Libraries.DBModel import *
from Libraries.Utils import *
from QQBot.QQBot import QQBot
from Speak.Speak import Speak
from Admin.Admin import Admin
from Secret.Secret import Secret
socketio = SocketIO()

def configure_blueprints(app):
    app.secret_key = 'jikappj39822@$*hjj'

    # 初始化数据库模型
    # DBModelFactory.instance()
    app.register_blueprint(Admin, url_prefix="/")
    app.register_blueprint(QQBot, url_prefix="/")
    app.register_blueprint(Speak, url_prefix="/")
    app.register_blueprint(Secret, url_prefix="/")

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

def create_app(debug=True):
    app = Flask('girlfriend')

    app.url_map.converters['regex'] = RegexConverter
    app.debug = debug
    Gzip(app)  # 使用gzip对响应进行压缩
    configure_blueprints(app)
    return app

app = create_app()
socketio.init_app(app)

# For debugging; will not run if launched from Nginx
if __name__ == "__main__":
    # app.run(port=8098, debug=True, host="0.0.0.0")#host0000可从外网访问
    socketio.run(app, debug=True, host="0.0.0.0",port=8098)
