# -*- coding: utf-8 -*-
import HTMLParser  

class MyHTMLParser(HTMLParser.HTMLParser):
    description_t = False
    name_t = False
    description_data = ""
    name_data = ""
    #处理开始标签，比如<xx>
    def handle_starttag(self, tag, attrs):
        # if str(tag).startswith("p"):
        #     for attr in attrs:
        #         if str(attr).find("description") != -1 and str(attr).find("itemprop") != -1:
        #             self.description_t=True
                    
        if str(tag).startswith("h1"):
            for attr in attrs:
                if str(attr).find("name") != -1 and str(attr).find("itemprop") != -1:
                    self.name_t=True
                    
    #处理<xx>data</xx>中间的那些数据
    def handle_data(self, data):
        if self.description_t is True:
            self.description_data = data 

        if self.name_t is True:
            self.name_data = data 

    #处理结束标签，比如</xx>或者<……/>
    def handle_endtag(self, tag):
        self.description_t=False
        self.name_t=False 

    def get_target_data(self):
        ret_name = self.name_data
        self.name_data = ""
        return {"name":ret_name}
