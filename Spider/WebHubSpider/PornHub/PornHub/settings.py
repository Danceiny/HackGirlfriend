# -*- coding: utf-8 -*-

# Scrapy settings for pornhub project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'PornHub'

SPIDER_MODULES = ['PornHub.spiders']
NEWSPIDER_MODULE = 'PornHub.spiders'

DOWNLOAD_DELAY = 1  # 间隔时间
# LOG_LEVEL = 'INFO'  # 日志级别
CONCURRENT_REQUESTS = 20  # 默认为16
# CONCURRENT_ITEMS = 1
# CONCURRENT_REQUESTS_PER_IP = 1
REDIRECT_ENABLED = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pornhub (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    "PornHub.middlewares.UserAgentMiddleware": 401,
    "PornHub.middlewares.CookiesMiddleware": 402,
}
ITEM_PIPELINES = {
    "PornHub.pipelines.PornhubMongoDBPipeline": 403,
}
