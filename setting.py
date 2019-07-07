# coding:utf-8

import logging

# 配置文件信息
MAX_SCORE = 10  # 代理ip的默认最高分值

# 日志配置信息
LOG_LEVEL = logging.DEBUG
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_FILENAME = 'log.log'

# 测试代理ip的超时时间
TEST_TIMEOUT = 5

# mongodb设置
MONGO_URL = 'mongodb://127.0.0.1:27017'

# 定义启动爬虫
PROXIES_SPDERS = [
    # 爬虫的全类名
    'proxy_spider.proxy_spiders.KuaidailiSpider',
    'proxy_spider.proxy_spiders.XiciSpider',
    'proxy_spider.proxy_spiders.YundailiSpider',
    'proxy_spider.proxy_spiders.SuperFastipSpider',
    'proxy_spider.proxy_spiders.QydailSpider',
    'proxy_spider.proxy_spiders.Dail89Spider',
]

# 自动启动程序爬取
RUN_SPDERS_INTERVAL = 1  # 分钟

# 配置异步数量
TEXT_PROXIES_AXYNC_COUT = 15

# 自动启动检测代理
TEXT_PROXIES_INTERVAL = 60 # 分钟

# 配置获取代理最大数量,越小可用性就越高,随机性越差
PROXIES_MAX_COUT = 50
