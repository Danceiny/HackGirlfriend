# -*- coding: utf-8 -*-
import HTMLParser  

class MyHTMLParser(HTMLParser.HTMLParser):
    description_t = False
    name_t = False
    description_data = ""
    name_data = ""
    #处理开始标签，比如<xx>
    def handle_starttag(self, tag, attrs):
        if str(tag).startswith("p"):
            for attr in attrs:
                if str(attr).find("description") != -1 and str(attr).find("itemprop") != -1:
                    self.description_t=True
                    
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
        return {"description":self.description_data,"name":self.name_data}


p=MyHTMLParser()
mystr = '''<head>
    <meta charset="utf-8"/>
    <title>aaaaaa</title>
     <p itemprop="description">aaaaaaaaaaaaa</p>
    <link rel="shortcut icon" href="/Content/Images/favicon.ico" type="image/x-icon"/>
    <meta content="技术搜索,IT搜索,程序搜索,代码搜索,程序员搜索引擎" name="keywords" />
    <meta content="面向程序员的专业搜索引擎。遇到技术问题怎么办，到博客园找找看..." name="description" />
    <link type="text/css" href="/Content/Style.css" rel="stylesheet" />
    <script src="http://common.cnblogs.com/script/jquery.js" type="text/javascript"></script>
    <script src="/Scripts/Common.js" type="text/javascript"></script>
    <script src="/Scripts/Home.js" type="text/javascript"></script>
</head>'''
p.feed(mystr)
print(p.get_target_data())
p.close()