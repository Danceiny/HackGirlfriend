# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import requests
from utils import datetime2timestamp, gen_attachment, trunc_utf8,COLORS,check_canvas
import random

Search_API = 'http://toutiao.com/search_content/?offset=0&format=json&keyword={0}&autoload=true&count={1}&_={2}'

def gen_attachment(text, image_url='', image_type='url', title='',
                   title_link='', color='random', fallback=True):
    if color == 'random':
        color = random.choice(COLORS)
    key = 'thumb_url' if image_type == 'thumb' else 'image_url'
    attachment = {'text': text, 'title_link': title_link, 'color': color,
                  key: check_canvas(image_url, image_type),
                  'title': title}
    if fallback:
        attachment.update({
            'fallback': u'{0} {1}'.format(
                convert2unicode(title), convert2unicode(text))
        })
    return attachment

def getSearchContent(data):
    requests_url = Search_API.format(data['keywords'],data['search_count'], datetime2timestamp())
    ret = requests.get(requests_url)
    data = ret.json()['data']

    count = 0
    for i in data:
        count = count + 1
        text = (u'<http://toutiao.com{seo_url}|{title}> 赞{digg_count} 踩{bury_count} - '
                '{source} {datetime}').format(**i)
        image_url = i.get('middle_image', '')
        if isinstance(image_url, dict):
            image_url = image_url['url']
        attach = gen_attachment(trunc_utf8(i['abstract']), image_url,
                                image_type='thumb', title=i['title'],
                                title_link=i['seo_url'], fallback=False)
        yield text, attach
    print("getSearchContent------count:%s" % repr(count))

def handle(data):
    ret = [r for r in getSearchContent(data)]
    result = '\n'.join([r[0] for r in ret]), [r[1] for r in ret]
    return result

if __name__ == '__main__':
    search_keyword = "视频"
    search_count  = 100
    result = handle({'keywords': search_keyword,'search_count':search_count})
    result = result[0].decode("utf-8") 
    f = open(r'result.txt', 'w') 
    f.write(result)
    f.close()


