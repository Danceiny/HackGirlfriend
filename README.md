# Hack Girlfriend

## 关于本项目 

[![](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/download/releases/3.4.0/) [![](https://img.shields.io/badge/python-3.5-green.svg)](https://www.python.org/downloads/release/python-352/)
 [![](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/ResolveWang)

**本项目是以flask为基础的后台项目，注重可扩展性，以学习为目的。**

## 服务器部署示例
以 腾讯云 Ubuntu 16 64bit 为例。

### Pre-requisites
- mysql-server / libmysqld
- nginx
- uwsgi
### Nginx + uWSGI
nginx配置 uwsgi_pass, 可以是sock文件，可以是ip:port。

/etc/nginx/conf.d/*.conf

uwsgi的配置文件socket=对应nginx的uwsgi_pass。

需要安装uwsgi-plugin-python。

uwsgi配置 uwsgi.ini:
```ini
socket = 
pythonpath = 
home = # venv / virtualenv / ...
plugin = python,http
...
```
### Common commands
- ps -ef | grep nginx
- service nginx start/reload/stop
- sudo ln -s nginx_uwsgi.conf /etc/nginx/conf.d/


## TODO LIST

- [ ] QQ Bot
    - 模块化： 进行中
    - 群聊监听保存聊天记录
    - 私聊机器人（图灵+其他）
- [ ] QQ Records Analysis
    - 対txt的私聊记录进行**时间、话题、情感**分析。
    - 对群聊记录进行分析
    - 自动化获取聊天记录
- [ ] 语音合成
    - [ ] 接入百度语音REST API
    - 接入讯飞API，需要做其他语言到python的桥接，待定
    - fmod api的python接口实现，难度较大，不如直接在其他平台原生实现。
    

# Refs
- https://github.com/xiyouMc/WebHubBot/

# Copyrights
Spring Oscillator 2017 &copy; Danceiny
All rights reserved.

项目中可能使用了某些开源代码，若未声明原作者，概疏忽所致，概不负责。

# Contributers 📢

## 协作隐私约定
    涉及账号密码等隐私信息的配置文件，请以'sec.*'为后缀名。
    
## 协作项目目录结构说明

### Applications
单个应用以flask-blueprint来做，在Applications里做路由转发。

### Platform
Applications转发到此（有一个对应关系）。

### Docs
项目中用到的技术，学习中可以留下**简要**的文档。

### Libraries
项目中用到的库（第三方或者自建）。

### PackageData
公用配置信息。（暂时还没太想好）

### Spider
项目中用到的爬虫。



## 协作者
- 
- 


