#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')   

import xlrd
import xlwt
from xlutils.copy import copy  
import urllib2
import urllib
import json
import codecs
from MyHTMLParser import MyHTMLParser

copyWriter = "auto_app_type_info.xls"
excel_data = xlrd.open_workbook(copyWriter)
read_sheet = excel_data.sheets()[0]
wb_book = copy(excel_data)  
wb_sheet = wb_book.get_sheet(0)

class AppStoreInfo():
    def __init__(self):
        self.appids = read_sheet.col_values(2)
        self.appnames = read_sheet.col_values(3)
        self.myHTMLParser=MyHTMLParser()

    def getAppInfo(self):
        base_url = "http://itunes.apple.com/app/id"
        # f = open(r'result.txt', 'w') 

        for index in range(0,len(self.appids)):
            app_id = self.appids[index]
            if len(app_id) < 8 or self.appnames[index] != '':
                continue  
            app_url = "%s%s" % (base_url,str(app_id))
            try:

                data = urllib2.urlopen(app_url).read()
                #设置解码方式
                data = data.decode('utf-8')
                
                self.myHTMLParser.feed(data)
                parser_data = self.myHTMLParser.get_target_data()
                app_name = parser_data['name']
                print("app_name:%s,app_id:%s" % (app_name,str(app_id)) )

                wb_sheet.write(index,3,app_name)
            except Exception, e:
                print("app_id:%s,error" % str(app_id))
            # f.write(data)
        # f.close()
        wb_book.save(copyWriter)
        self.myHTMLParser.close()

if __name__ == "__main__":
    appstoreInfo = AppStoreInfo()
    response = appstoreInfo.getAppInfo()
    print "the end"
