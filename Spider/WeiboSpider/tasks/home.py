# coding:utf-8
import time
from logger.log import crawler
from tasks.workers import app
from page_parse.user import public
from page_get.basic import get_page
from db.wb_data import insert_weibo_datas
from db.seed_ids import get_home_ids
from config.conf import get_max_home_page
from page_parse.home import get_wbdata_fromweb, get_home_wbdata_byajax, get_total_page


# 只抓取原创微博
home_url = 'http://weibo.com/u/{}?is_ori=1&is_tag=0&profile_ftype=1&page={}'
ajax_url = 'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain={}&pagebar={}&is_ori=1&id={}{}&page={}' \
           '&pre_page={}&__rnd={}'


@app.task(ignore_result=True)
def crawl_ajax_page(url):
    """
    返回值主要供第一次本地调用使用（获取总页数），网络调用忽略返回值
    :param url: 
    :return: 
    """
    ajax_html = get_page(url, user_verify=False)
    ajax_wbdatas = get_home_wbdata_byajax(ajax_html)
    if not ajax_wbdatas:
        return ''

    insert_weibo_datas(ajax_wbdatas)
    return ajax_html


@app.task(ignore_result=True)
def crawl_weibo_datas(uid):
    limit = get_max_home_page()
    cur_page = 1
    while cur_page <= limit:
        url = home_url.format(uid, cur_page)
        html = get_page(url)
        weibo_datas = get_wbdata_fromweb(html)

        if not weibo_datas:
            crawler.warning('用户id为{}的用户主页微博数据未采集成功，请检查原因'.format(uid))
            return

        insert_weibo_datas(weibo_datas)

        domain = public.get_userdomain(html)
        cur_time = int(time.time()*1000)
        ajax_url_0 = ajax_url.format(domain, 0, domain, uid, cur_page, cur_page, cur_time)
        ajax_url_1 = ajax_url.format(domain, 1, domain, uid, cur_page, cur_page, cur_time+100)

        if cur_page == 1:
            total_page = get_total_page(crawl_ajax_page(ajax_url_1))

        if total_page < limit:
            limit = total_page

        cur_page += 1
        app.send_task('tasks.home.crawl_ajax_page', args=(ajax_url_0,), queue='ajax_home_crawler',
                      routing_key='ajax_home_info')

        app.send_task('tasks.home.crawl_ajax_page', args=(ajax_url_1,), queue='ajax_home_crawler',
                      routing_key='ajax_home_info')


@app.task
def excute_home_task():
    # 这里的策略由自己指定，可以基于已有用户做主页抓取，也可以指定一些用户,我这里直接选的种子数据库中的uid
    id_objs = get_home_ids()
    for id_obj in id_objs:
        app.send_task('tasks.home.crawl_weibo_datas', args=(id_obj.uid,), queue='home_crawler',
                      routing_key='home_info')