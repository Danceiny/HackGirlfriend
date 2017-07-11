#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import traceback
import os, logging
import logging
import logging.config

from logging.handlers import RotatingFileHandler


import ConfigParser
conf = ConfigParser.ConfigParser()
conf_name = os.path.join('PackageData','logger.conf')
conf_path = os.path.dirname(os.path.dirname(__file__))
conf.read(os.path.join(conf_path,conf_name))
import platform
plat = platform.platform().lower()
home_key = 'HOME'
if 'windows' in plat:  # windows
    plat = "win"
    home_key = 'HOMEPATH'
elif 'darwin' in plat:
    plat = 'mac'
elif 'linux' in plat:
    plat = 'linux'
output_log_basepath = conf.get(plat,'output_log_basepath')
if conf.getboolean(plat,'log_at_home'):
    # 日志目录在家目录而不是/var/log等
    home_dir = os.environ[home_key]
    output_log_basepath = ''.join((home_dir,os.sep)) if not home_dir.endswith(os.sep) else home_dir

global_loggers = None


class MyLogger():
    def __init__(self, name):
        self.logger = self._get_logger(name, name)

    def debug(self, message):
        global_loggers.debug(message)
        self.logger.debug(message)

    def info(self, message):
        global_loggers.info(message)
        self.logger.info(message)

    def warning(self, message):
        global_loggers.warning(message)
        self.logger.warning(message)

    def error(self, message):
        global_loggers.error(message)
        self.logger.error(repr(traceback.format_exc()))
        self.logger.error(message)

    def _get_logger(self, logger_file, file):
        dir_path = '%s%s' % (output_log_basepath, logger_file)
        self._mkdir(dir_path)

        logger = logging.getLogger(logger_file)

        # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s]: %(filename)s[line:%(lineno)d] [pid:%(process)d] %(levelname)s %(message)s")
        console.setFormatter(formatter)
        logger.addHandler(console)

        # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大5M
        Rthandler = RotatingFileHandler('%s/%s.log' % (dir_path, file), maxBytes=5 * 1024 * 1024, backupCount=10)
        Rthandler.setLevel(logging.DEBUG)
        Rformatter = logging.Formatter(
            "[%(asctime)s]: %(filename)s[line:%(lineno)d] [pid:%(process)d] %(levelname)s %(message)s")
        Rthandler.setFormatter(Rformatter)
        logger.addHandler(Rthandler)

        logger.setLevel(logging.DEBUG)
        return logger

    def _mkdir(self, path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            return False

    def get_this_exception_info(self):
        '''获取当前异常出现的信息
        输出: result={'type':exc_type,'value':exc_value,'tb':exc_tb,'line_number':exc_tb.lineno}
            type：异常类型  value：异常值    tb:异常信息   line_number:异常行数'''
        exc_type, exc_value, exc_tb = sys.exc_info()
        result = {}
        result['type'] = exc_type
        result['value'] = exc_value
        result['exc_tb'] = exc_tb
        result['line_number'] = exc_tb.tb_lineno
        return result

    def get_exception_lineno(self):
        '''取出异常行数
        '''
        return self.get_this_exception_info()['line_number']


global_loggers = MyLogger('GlobalLog').logger