# coding=utf-8
import os
import re
import random
import shutil
import calendar
from datetime import datetime
import pytz
import requests

CANVAS_REGEX = re.compile(r'base64,(.*)')

ONE_MINUTE = 60
HALF_HOUR = 60 * 30
ONE_HOUR = 60 * 60
HALF_DAY = 60 * 60 * 12
ONE_DAY = 60 * 60 * 24

COLORS = (
    '#001f3f',  # Navy
    '#0074D9',  # Blue
    '#7FDBFF',  # Aqua
    '#39CCCC',  # Teal
    '#3D9970',  # Olive
    '#2ECC40',  # Green
    '#01FF70',  # Lime
    '#FFDC00',  # Yellow
    '#FF851B',  # Orange
    '#FF4136',  # Red
    '#85144b',  # Maroon
    '#F012BE',  # Fuchsia
    '#b10dc9',  # Purple
    '#111111',  # black
    '#aaaaaa',  # Gray
    '#dddddd',  # Silver
)

def check_cache(cache, fn, *args, **kwargs):
    timeout = kwargs.get('timeout', ONE_DAY)
    return (cache.cached(timeout=timeout)(fn)
            if cache is not None else fn)(*args, **kwargs)


def timestamp2str(timestamp, fmt='%H:%M:%S', timezone='Asia/Shanghai'):
    dt = datetime.utcfromtimestamp(float(timestamp)).replace(tzinfo=pytz.utc)
    tz = pytz.timezone(timezone)
    return tz.normalize(dt.astimezone(tz)).strftime(fmt)


def datetime2timestamp(dt=None, timezone='Asia/Shanghai'):
    if dt is None:
        dt = datetime.now()
    tz = pytz.timezone(timezone)
    dt = dt.replace(tzinfo=pytz.utc).astimezone(tz)
    return calendar.timegm(dt.timetuple())


def check_time(dt=None, timezone='Asia/Shanghai'):
    if dt is None:
        dt = datetime.now()
    tz = pytz.timezone(timezone)
    dt = dt.replace(tzinfo=pytz.utc).astimezone(tz)
    return 'day' if 6 <= dt.hour <= 18 else 'night'

def chinese2digit(ch):
    try:
        return ['一', '二', '三', '四', '五', '六', '七',
                '八', '九'].index(ch) + 1
    except ValueError:
        return ch


def upload_image(canvas_or_url, image_type, app=None, filename=None,
                 tmp_dir=None, deleted=False):
    pass
    
def check_canvas(image_url, image_type):
    match = CANVAS_REGEX.search(image_url)
    if match:
        return image_url #upload_image(image_url, image_type)
    else:
        return image_url


def convert2unicode(s):
    if not isinstance(s, unicode):
        return s.decode('utf-8')
    return s


def convert2str(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    return s


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


def trunc_utf8(s, length=50):
    s = convert2unicode(s)
    if s > length:
        s = s[:length] + '...'
    return s


def replaced(message, rep_words):
    for word in rep_words:
        message = message.replace(word, '', 1)
    return message
