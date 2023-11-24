import sys
from urllib.request import urlopen

from pip._vendor import requests
'''
工具类
'''


class UrlGetUtil:
    '''
    url 待抓取url
    tarBianMa 目标编码,eg： 'gbk'
    '''

    def getByRequestGet(self, url, tarBianMa):
        response = requests.get(url)
        #print(response.encoding) #查看现有编码
        response.encoding = tarBianMa  # 改变编码
        #print(response.encoding)#查看改变后的编码
        html = response.text
        return html

    '''
    url 待抓取url
    tarBianMa 目标编码,eg： 'gbk'
    '''

    def getByUrlOpen(self, url, tarBianMa):
        #10s超时
        html_obj = urlopen(url, timeout=10)
        html = html_obj.read().decode(tarBianMa)
        return html
