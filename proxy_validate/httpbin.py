# coding:utf-8
import time
import requests
import json
from utlis.http import get_request_headers
from setting import TEST_TIMEOUT
from utlis.log import logger
from ipmd import Proxy

def check_proxy(proxy):
    proxies = {
        'http': 'http://{}:{}'.format(proxy.ip, proxy.prot),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.prot)
    }
    http, http_nick_type, http_speed = __check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies, False)
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy

def __check_http_proxies(proxies, is_http=True):
    nick_type = -1
    speed = -1
    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'
    start = time.time()
    try:
        response = requests.get(test_url, headers=get_request_headers(), proxies=proxies, timeout=TEST_TIMEOUT)
        # print(response.content)
        if response.ok:
            speed = round(time.time() - start, 2)  # 响应速度
            dic = json.loads(response.text)
            # print(dic)
            origins = dic['origin']
            origin =origins.split(",")
            proxy_connection = dic['headers'].get('Cache-Control', None)
            if origin[0] == origin[1]:
                nick_type = 2
            elif proxy_connection:
                nick_type = 1
            else:
                nick_type = 0
            return True, nick_type, speed
        return False, nick_type, speed
    except Exception as ex:
        # logger.exception(ex)
        return False, nick_type, speed


if __name__ == '__main__':
    proxy = Proxy('39.98.189.213', prot='8888')
    print(check_proxy(proxy))