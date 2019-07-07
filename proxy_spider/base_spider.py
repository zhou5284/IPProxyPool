# coding:utf-8
import requests
from lxml import etree
from utlis.http import get_request_headers
from ipmd import Proxy


class BaseSpider(object):

    urls = []
    group_xpath = ''
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):

        if urls:
            self.urls = urls

        if group_xpath:
            self.group_xpath = group_xpath

        if detail_xpath:
            self.detail_xpath = detail_xpath


    def get_page_from_url(self, url):
        '''根据url获取页面数据'''
        response = requests.get(url, headers=get_request_headers())
        return response.content


    def get_first_from_list(self, lis):
        '''判断列表元素中是否含有元素,如果没有返回空字符串'''
        return lis[0] if len(lis) != 0 else ''


    def get_page_from_page(self, page):
        '''解析页面类容,返回proxy数据'''
        element = etree.HTML(page)
        trs = element.xpath(self.group_xpath)
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip'])).strip('\n\t')
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port'])).strip('\n\t')
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area'])).strip('\n\t')
            proxy = Proxy(ip, port, area=area)
            yield proxy


    def get_proxies(self):

        for url in self.urls:
            page = self.get_page_from_url(url)
            proxies = self.get_page_from_page(page)
            yield from proxies

if __name__ == '__main__':
    dic = {
        'urls': ['http://www.89ip.cn/index_{}.html'.format(i) for i in range(1, 11)],
        'group_xpath': '//*[@class="layui-table"]/tbody/tr',
        'detail_xpath': {
            'ip' : './td[1]/text()',
            'port' : './td[2]/text()',
            'area' : './td[3]/text()',
        }
    }

    spider = BaseSpider(**dic)
    for proxy in spider.get_proxies():
        print(proxy)