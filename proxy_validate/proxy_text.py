# coding:utf-8
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
import schedule
import time
from db.mongo_pool import MongoPool
from proxy_validate.httpbin import check_proxy
from setting import MAX_SCORE, TEXT_PROXIES_AXYNC_COUT, TEXT_PROXIES_INTERVAL


class ProxyTexter(object):

    def __init__(self):
        '''创建操作数据库的对象'''
        self.mongo_pool = MongoPool()
        self.queue = Queue()
        self.coroutine_proxy = Pool()

    def __check_callback(self, temp):
        # 死循环调用
        self.coroutine_proxy.apply_async(self.__check_noe_proxy, callback=self.__check_callback)

    def run(self):
        '''检测核心逻辑'''
        proxies = self.mongo_pool.find_all()

        for proxy in proxies:
            # 检测
            # self.__check_noe_proxy(proxy)
            # 把代理添加到队列中
            self.queue.put(proxy)
        # 异步
        for i in range(TEXT_PROXIES_AXYNC_COUT):
            # 异步回调
            self.coroutine_proxy.apply_async(self.__check_noe_proxy, callback=self.__check_callback)
        # 让当前的 线程 等待 队列任务的完成
        self.queue.join()

    def __check_noe_proxy(self):
        '''处理单个代理'''
        # 获取队列中的代理
        proxy = self.queue.get()
        proxy = check_proxy(proxy)
        if proxy.speed == -1:
            proxy.score -= 1
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            else:
                self.mongo_pool.delete_one(proxy)
        else:
            proxy.score = MAX_SCORE
            self.mongo_pool.delete_one(proxy)
        # 调度队列的task_done方法
        self.queue.task_done()

    @classmethod
    def start(cls):
        '''运行时间设定,制动执行'''
        proxy_tester = cls()
        proxy_tester.run()
        # schedule.every(TEXT_PROXIES_INTERVAL).hour.do(proxy_tester.run)  # 每多少小时检测一次
        schedule.every(TEXT_PROXIES_INTERVAL).minutes.do(proxy_tester.run)  # 每多少分钟检测一次
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    # pt = ProxyTexter()
    # pt.run()
    ProxyTexter.start()
