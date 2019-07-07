# coding:utf-8
from flask import Flask
from flask import request
import json
from db.mongo_pool import MongoPool
from setting import PROXIES_MAX_COUT


class ProxyAip(object):

    def __init__(self):

        self.app = Flask(__name__)
        self.mongo = MongoPool()

        @self.app.route('/')
        def hello_world():
            tips = '/random?protocol&domain&count'

            return tips

        # 随机获取一个代理
        @self.app.route('/random')
        def random():
            # 获取协议
            protocol = request.args.get('protocol')
            # 获取域名
            domain = request.args.get('domain')
            proxy = self.mongo.random_proxy(protocol, domain, count=PROXIES_MAX_COUT)

            if protocol:
                return '{}://{}:{}'.format(protocol, proxy.ip, proxy.prot)
            else:
                return '{}:{}'.format(proxy.ip, proxy.prot)

        # 获取队列中代理
        @self.app.route('/proxies')
        def proxies():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxies = self.mongo.get_proxies(protocol, domain, count=PROXIES_MAX_COUT)
            proxies = [proxy.__dict__ for proxy in proxies]

            return json.dumps(proxies)

        # 获取过滤掉不可用域名的代理
        @self.app.route('/disable_domain')
        def disable_domain():

            ip = request.args.get('ip')
            domain = request.args.get('domain')
            if ip is None:
                return '提供ip参数'
            if domain is None:
                return '提供domian参数'
            self.mongo.disable_domain(ip, domain)
            return '{}禁用()成功!'.format(ip, domain)

    def run(self):
        self.app.run('127.0.0.1', port=8000)

    @classmethod
    def start(cls):
        proxy_api = ProxyAip()
        proxy_api.run()


if __name__ == '__main__':
    ProxyAip.start()
