#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ConfigParser(object):
    """Implementation of config center
    """
    def __init__(self, configs, file):
        self._configs = configs
        self._file = file

    def _check_key(self, section, key=None):
        if not self._configs.has_key(section):
            raise KeyError, 'section "%s" not in "%s". configs=[%s]' % (section, self._file, repr(self._configs))
        if key is not None and not self._configs[section].has_key(key):
            raise KeyError, 'key "%s" not in section "%s" of "%s". configs=[%s]' % (key, section, self._file, repr(self._configs))

    def get(self, section, key):
        self._check_key(section, key)
        return self._configs[section][key]

    def getint(self, section, key):
        self._check_key(section, key)
        return int(self._configs[section][key])

    def getfloat(self, section, key):
        self._check_key(section, key)
        return float(self._configs[section][key])

    def getboolean(self, section, key):
        self._check_key(section, key)
        value = self._configs[section][key]
        return value.lower() != 'false' and value != '0'

    def items(self, section):
        self._check_key(section)
        return self._configs[section]