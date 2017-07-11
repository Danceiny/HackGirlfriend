# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

import codecs
import re
import json

READ_CACHE_LINES = 10000

def load_FILE_conf(debug=False):
    with codecs.open('FILE.conf.sec.txt', 'r', 'utf-8') as f:
        variables = {}
        for line in f.readlines():
            print line
            names = line.split('=')
            if not variables.has_key(names[0].strip()):
                variables[names[0].strip()] = names[1].strip()
            globals()[names[0].strip()] = names[1].strip()  # 加载到全局变量中
        return variables

if __name__ == '__main__':
    load_FILE_conf()

def get_records_from_json_file(filename,debug=False):
    with codecs.open(filename, 'r','utf-8') as f:
        return list(json.loads(f.read()))


def get_records_from_raw_qqchat_file(filename,debug=False):
    '''

    :param filename: raw qqchat file
    :param debug: print information
    :return: records, dict
    '''
    records = []
    # record = {'time':'','user':'','sentence':''}
    record = {}
    record_header = {'group': '', 'person': ''}
    with codecs.open(filename, 'r','utf-8') as f:
        lines = f.readlines()
        if not lines:
            if debug:print 'blank line'
        i = 0
        lastline = None
        for line in lines:
            i += 1
            if i <= 2:
                continue#头两行是不重要信息
            if str(line).startswith(u'消息分组'):
                # print line[5:]
                record_header['group'] = line[5:]
            if str(line).startswith(u'消息对象'):
                # print line[5:]
                record_header['person'] = line[5:]
            if str(line).startswith('==='):
                # print '==='
                continue
            if re.match(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}',line):
                record['str_time'] = line[:19].strip()
                if debug:print record['str_time']
                record['int_time'] = int(time.mktime(time.strptime(str(record['str_time']),'%Y-%m-%d %H:%M:%S')))
                record['user'] = line[19:].strip()
                # print 'time',record['time'],record['user']
                continue
            if line == None or line.strip() == '' or str(line).startswith(' '):
                # print '空行'
                if lastline != line:
                    if debug:print '新一条聊天记录'
                    if record.has_key('str_time') and record.has_key('sentence') and record.has_key('user'):
                        records.append(record)
                        record = {}
                continue

            # record['sentence'] = str(line).strip()
            record['sentence'] = line.strip()
            # print type(record['sentence']),record['sentence']
            if debug:print 'sentence',record['sentence']
            lastline = line
    return record_header,records

def write_records_with_json(records,filename):
    '''
    :param records: list, item=dict, unicode/utf-8
    :param filename: str, output file
    :return: none
    '''
    with codecs.open(filename, 'wb', 'utf-8') as f:
        f.write(json.dumps(records,ensure_ascii=False))
    #     for index in xrange(len(records)):
    #         record = records[index]
    #         # print 'record, stat time',type(record['sentence']),type(record['str_time']),type(record['user'])
    #         # print str(record['str_time'])
    #         # tu = time.strptime(str(record['str_time']), '%Y-%m-%d %H:%M:%S')
    #         # print tu
    #         # print time.mktime(tu)
    #         # record['int_time'] = int(time.mktime(tu))
    #         # record['int_time'] = utils.convert_string_2_int(record['str_time'])
    #         # print record['int_time']
    #         # print unicode(json.dumps(record)).encode('utf-8')
    #         # print 'no encode',unicode(json.dumps(record))
    #
    #         f.write(json.dumps(record,ensure_ascii=False))#record is unicode!!!
    #         f.write('\n')

