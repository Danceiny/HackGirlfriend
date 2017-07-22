#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import Libraries.ErrorDefine as ED

from Libraries.Singleton.Singleton import Singleton

from Libraries.DBModel import *
from Platform.LogCenter.LogCenter import LogCenter

@Singleton
class ChatbotCenter(object):
    def __init__(self, conf_file = None):
        self.db_model = DBModelFactory.instance().get_db_model()
        self.db_model_read = DBModelFactory.instance().get_db_model(readonly=True)
        self.logger = LogCenter.instance().get_logger('ExceptionLog')


    def simple_reply(self,data):
        result = {'code': ED.no_err}
        sentence = data.get('sent')
        result['data'] = self.segment_sentence(sentence)
        return result

    def segment_sentence(self,sentence):
        ret = ''
        import pynlpir
        pynlpir.open()
        segments = pynlpir.segment(sentence,pos_names='all',pos_english=False)
        for segment in segments:
            ret += '\t'.join(( segment[0], segment[1]))
            ret += '\n'

        pynlpir.close()
        return ret

    def update_config(self, data):
        result = {'code': ED.no_err}

        return result

    def add_config(self, data):
        result = {'code': ED.no_err}

        return result


    def get_configs(self,file=None, section=None, key=None, pid=None):
        result = {'code': ED.no_err}

        return result