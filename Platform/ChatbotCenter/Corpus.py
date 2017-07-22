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
class Corpus(object):
    def __init__(self, conf_file = None):
        self.db_model = DBModelFactory.instance().get_db_model()
        self.db_model_read = DBModelFactory.instance().get_db_model(readonly=True)
        self.logger = LogCenter.instance().get_logger('CorpusLog')


    def simple_reply(self,data):
        result = {'code': ED.no_err}
        sentence = data.get('sent')
        result['data'] = self.segment_sentence(sentence)
        return result

