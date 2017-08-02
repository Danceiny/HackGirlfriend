# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
# from PackageNormalData import *
from flask import Blueprint, request, jsonify, redirect, render_template

import platform
if 'win' in platform.platform().lower():
    import pylab
from scipy.io import wavfile
import Libraries.ErrorDefine as ED

from Libraries.Singleton.Singleton import Singleton
from Libraries.DBModel import *
from Platform.LogCenter.LogCenter import LogCenter

@Singleton
class SpeakCenter(object):
    def __init__(self, conf_file = None):
        self.db_model = DBModelFactory.instance().get_db_model()
        self.db_model_read = DBModelFactory.instance().get_db_model(readonly=True)
        self.logger = LogCenter.instance().get_logger('ExceptionLog')


    def delete_config(self,data):
        result = {'code': ED.no_err}
        import pynlpir

        pynlpir.open()
        sentence = data.get('sent')
        segments = pynlpir.segment(sentence)
        for segment in segments:
            print segment[0], '\t', segment[1]

        pynlpir.close()
        return result

    def update_config(self, data):
        result = {'code': ED.no_err}

        return result

    def add_config(self, data):
        result = {'code': ED.no_err}

        return result


    def get_configs(self,file=None, section=None, key=None, pid=None):
        result = {'code': ED.no_err}

        return result


class GirlVoice():
    def __init__(self,raw_voice_robot,params=None):
        #TODO: raw_voice_robot 可以是文件（文件类型），也可以是比特流
        self.raw_voice_robot = raw_voice_robot

    def getBasicPropertyOfVoice(self,voice):
        sampFreq, snd = wavfile.read(voice)
        return snd.dtype, snd.shape

    def getBasicProcessedVoice(self,raw_voice):
        sampFreq, snd = wavfile.read(raw_voice)
        return voice