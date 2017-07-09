#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'Danceiny'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import codecs
import requests
import urllib,urllib2
import pickle
import pickletools
import requests
from lxml import etree
import time
RAND_RANGE = (1000,10000)

import random
from Configs import *

class ArticleParser:
    def __init__(self,tree=None,url_example=''):
        self.tree = tree
        self.url_example = url_example

class HupuPostParser(ArticleParser):
    # html.decode('utf-8', 'ignore')
    # self.url_example = https://bbs.hupu.com/19453374.html
    def parse_post_content(self,tree,debug=True):
        titleElement = tree.find('.//div/h1[@id="j_data"]')
        title = titleElement.attrib.get('data-title','')
        fidname = titleElement.attrib.get('fidname','') #影视区
        replyStat = titleElement.attrib.get('data-replies','')
        statsElement = tree.find('.//div/span')
        stats = statsElement.text.decode('utf-8')
        print stats

        authorElement = tree.find('.//div[@class="author"]')
        hupuIdElement = authorElement.find('.//a[@class="u"]')
        # print authorElement,dir(authorElement)
        # print hrefs[0].attrib
        personalHomepage = hupuIdElement.attrib.get('href','')
        print personalHomepage

        hupuGradeElement = authorElement.find('.//span/a')


        personalPosts = hupuGradeElement.attrib.get('href','')
        hupuGrade = hupuGradeElement.text   # '32级' 汉字乱码

        print personalPosts,hupuGrade

        pubTimeElement = authorElement.xpath('//span[@class="stime"]')
        if type(pubTimeElement) == list:
            pubTime = pubTimeElement[0].text    #2017-06-16 21:11
        print pubTime
        pass

        quoteContentElement = tree.xpath('.//div[@class="quote-content"]')
        print len(quoteContentElement)
        content = ''
        for para in quoteContentElement:
            content += etree.tostring(para,pretty_print=True,method='html',encoding='utf-8')

        floors = tree.find('.//div[@id="readfloor"]')
        i = 0
        for floor in floors:
            i+=1
            replyerHupuId = floor.xpath('.//div[@class="user"]/div/@uname')[0]
            # .atrrib.get('uname','')
            floorBox = floor.find('.//div[@class="floor_box"]')
            replyTime = floorBox.find('.//span[@class="stime"]').text
            highlightsStat = floorBox.find('.//span[@class="ilike_icon_list"]/span[@class="stime"]').text

            replyContent = floorBox.find('.//table/tbody')
            print "第 ", i, " 楼",replyerHupuId,replyTime,highlightsStat,replyContent


    def get_more_urls(self,tree,debug=True):
        pass
    pass

class KexuewangBlogParser(ArticleParser):
    # self.url_example = http://blog.sciencenet.cn/blog-117889-804430.html
    def parse_blog_content(self, tree, debug=True):
        articleElement = tree.find('.//div[@id="blog_article"]')
        titleElement = tree.find('.//h1[@class="ph"]')
        title = titleElement.text.strip()
        print 'title',title
        subtitleElement = tree.xpath('.//p[@class="xg2"]/span[@class="xg1"]')
        print subtitleElement
        hits = subtitleElement[0].text.strip()[2:][:-3].strip() #已有 18570 次阅读
        print 'hits',hits
        update_time = subtitleElement[1].text.strip()   # 2016-1-17 10:39
        print 'update_time',update_time
        tags = {}
        for el in subtitleElement[2:]:
            print 'el',el,dir(el)
            tagEl = el.xpath('./text()')
            tagValue = el.xpath('./a')
            # print 'tagValue dir',dir(tagValue)
            if len(tagValue)>0:
                # print 'a tag value',tagValue[0].text
                # print 'tagEl',tagEl,dir(tagEl),tagEl[0]
                tags[tagEl[0].strip()] = tagValue[0]
            else:
                tagKey,tagValue = tagEl[0].split(':')
                print '%s=%s'%(tagKey,tagValue)
        parasElement = articleElement.xpath('.//p')
        content = ''
        for para in parasElement:
            content += etree.tostring(para,pretty_print=True,method='html',encoding='utf-8')
        return title,hits,update_time,content

class OldCecctmArticlesParser(ArticleParser):
    ############## crawler and parser  ##############
    # self.url_example = 'http://old.cecctm.com/news.asp?id=796'
    def parse_news_content(self,tree):
        # // *[ @ id = "txtCont"]
        catElement = tree.findall('.//div[@class="inNavR"]/a[@href]')
        category = str(catElement[1].text).strip()
        # print 'category',category

        contentElement = tree.find('.//div[@id="txtCont"]')

        titleElement = contentElement.find('.//p[@class="title"]')
        title = str(titleElement.text).strip()
        # print 'title',title

        subtitle = contentElement.xpath('.//div[@class="subtxt"]')

        hitsElement = subtitle[0].find('.//span')
        hits = int(str(hitsElement.text).strip())
        # print 'hits',hits

        # // *[ @ id = "txtCont"] / div / text()[2]
        show_time = subtitle[0].xpath('./text()')[1].strip()[-10:]

        parasElement = contentElement.xpath('./p')
        # print parasElement,parasElement[0]
        content = ''
        for para in parasElement:
            content += etree.tostring(para,pretty_print=True,method='html',encoding='utf-8')

        # content = etree.tostring(contentElement, pretty_print=True,method='html',encoding='utf-8')
        content = content.strip()
        return category,title,content,show_time,hits


    def normalize_news_sql_values(self,values):
        # a_id = random.randint(*RAND_RANGE)
        category = CATE_MAP.get(values[0],u'xwzx')
        title = values[1].decode('utf-8')
        content = values[2].decode('utf-8')
        if not content.endswith('</p>'):
            content += '</p>'
        show_time = int(time.mktime(time.strptime(values[3],'%Y-%m-%d')))
        # hits = random.randint(values[4],10*values[4]+10)
        # return a_id,category,title,content,show_time,hits
        return category,title,content,show_time

    def get_least_sql_values_dict(self,values):
        # GRABED_CONTENT_KEY = ('category', 'title', 'content', 'show_time')
        return dict((name, value) for name, value in zip(GRABED_CONTENT_KEY, values))