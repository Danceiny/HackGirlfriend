# -*- coding: utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))#把HackGirlfriend目录加载到$PYTHONPATH中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask
from flask_gzip import Gzip
import jinja2
from werkzeug.routing import BaseConverter
from flask_socketio import SocketIO
from Libraries.DBModel import *
from Libraries.Utils import *
from QQBot.QQBot import QQBot
from Speak.Speak import Speak
from Admin.Admin import Admin
from Secret.Secret import Secret
from Zuiwan.User import ZuiwanUser
from Zuiwan.Wechat import ZuiwanWechat
def configure_blueprints(app):
    app.secret_key = 'jikappj39822@$*hjj'

    # 初始化数据库模型
    # DBModelFactory.instance()
    app.register_blueprint(Admin, url_prefix="/")   # 总管理
    app.register_blueprint(QQBot, url_prefix="/")   # QQ机器人
    app.register_blueprint(Speak, url_prefix="/")   # 语音聊天
    app.register_blueprint(Secret, url_prefix="/")  # Secret Android API

    # zuiwan
    app.register_blueprint(ZuiwanWechat, url_prefix="/")
    app.register_blueprint(ZuiwanUser, url_prefix="/")

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

def create_app(debug=True):
    template_folder = os.path.abspath('Applications/static/templates')
    static_folder = os.path.abspath('Applications/static')

    # 事实上，windows
    import platform
    if 'windows' in platform.platform().lower():
        print('WARNING: in Windows Platform, you must declare templates_folder when instantiate blueprint, withing \
        relative path, usually "templates".')
    # 绝对路径！！！必须以/开头
    app = Flask('HackGirlfriend',static_folder=static_folder,template_folder = template_folder)
    # app = Flask('HackGirlfriend')

    app.url_map.converters['regex'] = RegexConverter
    app.debug = debug
    Gzip(app)  # 使用gzip对响应进行压缩
    configure_blueprints(app)

    # my_loader = jinja2.ChoiceLoader([
    #     app.jinja_loader,
    #     jinja2.FileSystemLoader([template_folder]),
    # ])
    # app.jinja_loader = my_loader


    return app

app = create_app()

# For debugging; will not run if launched from Nginx
if __name__ == "__main__":
    # socketio = SocketIO()
    # socketio.init_app(app)
    # # app.run(port=8098, debug=True, host="0.0.0.0")#host0000可从外网访问
    # socketio.run(app, debug=True, host="0.0.0.0",port=8098)

    app.run(port=8098, debug=True, host="0.0.0.0")#host0000可从外网访问


