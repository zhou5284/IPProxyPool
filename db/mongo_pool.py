# coding:utf-8
from pymongo import MongoClient
import pymongo
import random
from setting import MONGO_URL
from utlis.log import logger
from ipmd import Proxy



class MongoPool(object):

    def __init__(self):
        '''mongodb'''
        # 建立链接
        self.cloent = MongoClient(MONGO_URL)
        # 获取操作集合
        self.proxies = self.cloent['proxies_pool']['proxies']


    def __del__(self):
        '''关闭数据库链接'''
        self.cloent.close()


    # 增删改查
    def insert_one(self,proxy):
        '''插入/去重'''
        count = self.proxies.count({'_id':proxy.ip})
        if count == 0:
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info('代理新插入:{}'.format(proxy))
        else:
            logger.info('代理已存在:{}'.format(proxy))


    def update_one(self, proxy):
        '''更新功能'''
        self.proxies.update_one({'_id':proxy.ip},{'$set':proxy.__dict__})
        logger.info('代理已更新:{}'.format(proxy))

    def delete_one(self,proxy):
        '''删除功能'''
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info('代理已删除:{}'.format(proxy))


    def find_all(self):
        '''查询功能'''
        cursor = self.proxies.find()
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy


    def find(self, conditions={}, count=0):
        # print(conditions)
        '''API实现'''
        cursor = self.proxies.find(conditions, limit=count).sort([('score',pymongo.DESCENDING),('speed', pymongo.ASCENDING)]) # 实现顺序排列
        proxy_list = []
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list


    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        '''根据协议类型 和 要访问的网站域名,获取对应的ip代理'''
        #定义查询条件
        conditions = {'nick_type':nick_type}
        # 根据协议,指定查询条件

            # 没有传入协议类型,返回支持http/https协议
        if protocol is None:
            conditions['protocol'] = {'$in':[0, 1, 2]}
        elif protocol.lower() == 'http':
            conditions['protocol'] = {'$in':[0, 2]}
        else:
            conditions['protocol'] = {'$in':[1, 2]}

        if domain:
            conditions['disable_domains'] = {'$nin':[domain]}

        return self.find(conditions, count=count)


    def random_proxy(self, protocol=None, domain=None, count=0, nick_type=0):
        '''随机返回满足要求的一个ip代理'''
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, count=count, nick_type=nick_type)
        # print(proxy_list)
        return random.choice(proxy_list)


    def disable_domains(self, ip, domain):
        '''添加指定域名信息到disable_domains列表中'''

        if self.proxies.count({'_id':ip,'disable_domains':domain}) == 0:
            self.proxies.update_one({'_id':ip},{'$push':{'disable_domains':domain}})

            return True
        return False



if __name__ == '__main__':

    mongo = MongoPool()
    # proxy = Proxy('39.98.189.211', prot='1111')
    # mongo.insert_one(proxy)
    # proxy = Proxy('39.98.189.212', prot='2222')
    # mongo.insert_one(proxy)
    # proxy = Proxy('39.98.189.213', prot='3333')
    # mongo.insert_one(proxy)
    # proxy = Proxy('39.98.189.214', prot='4444')
    # mongo.insert_one(proxy)
    # for porxy in mongo.find_all():
    #     print(porxy)
    # proxy = Proxy('39.98.189.213', prot='5555')
    # mongo.update_one(proxy)
    # proxy = Proxy('39.98.189.214', prot='4444')
    # mongo.delete_one(proxy)
    # proxy = Proxy('39.98.189.212', prot='2222')
    # mongo.delete_one(proxy)
    # proxy = Proxy('39.98.189.213', prot='5555')
    # mongo.delete_one(proxy)
    # proxy = Proxy('39.98.189.214', prot='4444')
    # mongo.delete_one(proxy)

    # for proxy in mongo.find({'nick_type': 0, 'protocol': {'$in': [0, 2]}}):
    #     print(proxy)

    # proxy = Proxy(**dic)
    # mongo.insert_one(proxy)
    #
    # for proxy in mongo.get_proxies(protocol='http'):
    #     print(proxy)
    # print(mongo.disable_domains('39.98.189.215', 'taobao.com'))


