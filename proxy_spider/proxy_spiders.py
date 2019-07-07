# coding:utf-8
import random
import time
import requests
from lxml import etree
from proxy_spider.base_spider import BaseSpider
from utlis.http import get_request_headers
from ipmd import Proxy


class KuaidailiSpider(BaseSpider):
    # url队列
    urls = ['https://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 8)]
    # 分组的xpath
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内的xpath
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }

    # 方法重写
    def get_page_from_url(self, url):
        '''反爬机制,方法重写.等待1-3秒'''
        # time.sleep(random.uniform(1, 3))
        time.sleep(1)
        # 调用父类方法
        return super().get_page_from_url(url)


class XiciSpider(BaseSpider):
    # url队列
    urls = ['https://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 11)]
    # 分组的xpath
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'  # position()>1 过滤掉第一项,应为表头信息不需要
    # 组内的xpath
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[4]/a/text()',
    }


class YundailiSpider(BaseSpider):
    # url队列
    urls = ['http://www.ip3366.net/free/?stype={}&page={}'.format(i, j) for i in range(1, 5, 2) for j in range(1, 8)]
    # 分组的xpath
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内的xpath
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }


class SuperFastipSpider(BaseSpider):
    # url队列
    urls = ['http://www.superfastip.com/welcome/freeip/{}'.format(i) for i in range(1, 11)]
    # 分组的xpath
    group_xpath = '/html/body/div[3]/div/div/div[2]/div/table/tbody/tr'
    # 组内的xpath
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }

    def get_page_from_url(self, url):
        '''根据url获取页面数据'''
        response = requests.get(url, headers=get_request_headers())
        return response.content.decode('utf-8')


class QydailSpider(BaseSpider):
    # url队列
    urls = ['http://www.qydaili.com/free/?action=china&page={}'.format(i) for i in range(1, 11)]
    # 分组的xpath
    group_xpath = '//*[@id="content"]/section/div[2]/table/tbody/tr'
    # 组内的xpath
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }


class Dail89Spider(BaseSpider):
    # url队列
    urls = ['http://www.89ip.cn/index_{}.html'.format(i) for i in range(1, 11)]
    # 分组的xpath
    group_xpath = '//*[@class="layui-table"]/tbody/tr'
    # 组内的xpath
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }
    def get_page_from_url(self, url):
        '''根据url获取页面数据'''
        response = requests.get(url, headers=get_request_headers())
        return response.content.decode('utf-8')

if __name__ == '__main__':
    spider = Dail89Spider()
    for proxy in spider.get_proxies():
        print(proxy)
