# coding:utf-8
from setting import MAX_SCORE


class Proxy(object):
    '''代理ip的字段'''
    def __init__(self, ip, prot, protocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE, disable_domains=[]):
        self.ip = ip  # 代理ip
        self.prot = prot  # 代理ip端口
        self.protocol = protocol  # 代理ip支持的协议类型
        self.nick_type = nick_type  # 代理ip的匿名程度
        self.speed = speed  # 代理ip的响应速度
        self.area = area  # 代理ip的位置
        self.score = score  # 代理ip的评分
        self.disable_domains = disable_domains  # 不可用代理ip
    def __str__(self):
        # 返回数据字符串
        return str(self.__dict__)