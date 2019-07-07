# coding:utf-8
import importlib
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
import time
import schedule

from setting import PROXIES_SPDERS
from proxy_validate.httpbin import check_proxy
from db.mongo_pool import MongoPool
from utlis.log import logger
from setting import RUN_SPDERS_INTERVAL


class RunSpider(object):
    """启动spider"""

    def __init__(self):
        '''创建数据库对象'''
        self.mongo_pool = MongoPool()
        # 创建协程池
        self.coroutine_pool = Pool()

    def get_spider_from_settings(self):
        '''根据配置信息,获取爬虫列表'''
        for full_class_name in PROXIES_SPDERS:
            module_name, class_name = full_class_name.rsplit('.', maxsplit=1)  # 从左往右截1次
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            spdier = cls()

            yield spdier

    def run(self):

        spdiers = self.get_spider_from_settings()

        for spider in spdiers:
            # self.__execute_one_spider_task(spider)
            # 通过一部的方法执行
            self.coroutine_pool.apply_async(self.__execute_one_spider_task, args=(spider,))
        # 调用join方法,当前线程 等待 协程 任务的完成
        self.coroutine_pool.join()

    def __execute_one_spider_task(self, spider):
        '''把处理一个代理爬虫的代码抽到一个方法'''
        try:
            for proxy in spider.get_proxies():
                proxy = check_proxy(proxy)
                # print(proxy)
                # 写入数据库
                self.mongo_pool.insert_one(proxy)
        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def start(cls):
        '''运行时间设定,制动执行'''
        rs = RunSpider()
        rs.run()
        # schedule.every(RUN_SPDERS_INTERVAL).hour.do(rs.run)  # 小时
        schedule.every(RUN_SPDERS_INTERVAL).minutes.do(rs.run) # 分钟

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    # re = RunSpider()
    # re.run()
    RunSpider.start()
