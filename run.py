# coding:utf-8
from multiprocessing import Process
from proxy_spider.run_spider import RunSpider
from proxy_validate.proxy_text import ProxyTexter
from proxy_validate.proxy_api import ProxyAip


def run():
    process_list = []
    # 爬虫
    process_list.append(Process(target=RunSpider.start))
    # 检测
    process_list.append(Process(target=ProxyTexter.start))
    # API
    process_list.append(Process(target=ProxyAip.start))

    for process in process_list:
        # 设置守护进程
        process.daemon = True
        # 启动
        process.start()

    # 遍历进程列表,让主进程等待子进程任务的完成
    for process in process_list:
        process.join()


if __name__ == '__main__':
    run()
