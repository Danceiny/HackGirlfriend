#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from FileUtils import *
import os
import json

from Libraries.Singleton.Singleton import Singleton

@Singleton
class TextCenter():
    def __init__(self):
        self.texts = {}
        self.basePath = os.path.split(os.path.realpath(__file__))[0]
        lan_file_list = GetFileList("%s/Texts/" % self.basePath, ["txt"])
        for lan_file_name in lan_file_list:
            language = lan_file_name.split(".")[0]
            self.texts[language] = self._load_text_map(language)
        self.default_lan = 'en' #默认语言

    def get(self, key, lan):
        key = str(key)
        lan = str(lan).replace("-", "_")

        if not self.texts.has_key(lan):
            lan = self.default_lan

        texts_map = self.texts[lan]

        if not texts_map.has_key(key):
            if self.texts[self.default_lan].has_key(key):
                return self.texts[self.default_lan][key]
            else:
                return key

        return texts_map[key]

    def get_default_lan(self):
        return self.default_lan

    def set_default_lan(self, lan):
        lan = str(lan)
        if self.texts.has_key(lan):
            self.default_lan = lan

    def _load_text_map(self, lan):
        file_path = "%s/Texts/%s.txt" % (self.basePath, lan)
        if os.path.isfile(file_path):
            input_text = open(file_path).read()
            input_json = "{%(input_text)s}" % vars()
            text_map = json.loads(input_json)
            return text_map
        return {}