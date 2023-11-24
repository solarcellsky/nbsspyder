'''
    多层级循环递归调用解析区域，然后返回数据集合
'''
import socket
import time
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from Bean.NbsRegionDTO import NbsRegionDTO

from Bean.ParseErrorClass import ParseErrorClass
from Util.UrlGetUtil import UrlGetUtil


def cycleSpider(parent_code, parent_level, to_parse_url, error_data_set):
    # 本次爬取行政区划数据结果集
    tar_obj_set = set()
    #按层级使用不同的解析标签关键字
    tr_flag = ''
    current_level = parent_level + 1  #级别级别
    if current_level == 2:
        tr_flag = 'citytr'
    elif current_level == 3:
        tr_flag = 'countytr'
    elif current_level == 4:
        tr_flag = 'towntr'
    elif current_level == 5:
        tr_flag = 'villagetr'
    else:
        pass
    #解析
    try:
        urlGetUtilObj = UrlGetUtil()
        # urlopern方式
        html = urlGetUtilObj.getByUrlOpen(to_parse_url, 'gbk')
        # request.get 方式
        # html = urlGetUtilObj.getByRequestGet(to_parse_url,'gbk')
    except socket.timeout:
        print('parent_code = ' + parent_code + '---待解析URL：' + to_parse_url +
              '请求超时')
        # 暂时跳过，将出现异常的待解析数据暂存起来
        error_data_set.add(
            ParseErrorClass(parent_code, parent_level, to_parse_url))
        return tar_obj_set
    except HTTPError as e:
        print('parent_code = ' + parent_code + '---待解析URL：' + to_parse_url +
              '出现http错误:')
        print(e)
        # 暂时跳过，将出现异常的待解析数据暂存起来
        error_data_set.add(
            ParseErrorClass(parent_code, parent_level, to_parse_url))
        return tar_obj_set
    except Exception as e:
        print('parent_code = ' + parent_code + '---待解析URL：' + to_parse_url +
              '请求出现异常')
        print(e)
        #暂时跳过，将出现异常的待解析数据暂存起来
        error_data_set.add(
            ParseErrorClass(parent_code, parent_level, to_parse_url))
        return tar_obj_set
    else:
        pass
    bs = BeautifulSoup(html, 'html.parser')
    #获取本页所有数据节点
    trs = bs.findAll('tr', {'class': tr_flag})
    for tr in trs:
        #注意，5极页面有三个td，和别的等级页面中的相同td位置，存放数据不是一样的类型，所以进行判断
        td_1 = tr.find('td')  #第一个td节点
        current_code = td_1.get_text()
        current_url = ''
        current_name = ''
        current_town_country_code = ''
        td_2 = td_1.next_sibling  #第二个td节点
        if (current_level == 5):
            current_town_country_code = td_2.get_text()
            current_name = td_2.next_sibling.get_text()
        else:
            td_1_a = td_1.a
            if td_1_a is not None:  #比如青海省西宁市市辖区 ,才到三级，就咩有下级了，所以a标签为None对象
                current_url = td_1_a['href']
            current_name = td_2.get_text()
        #打印开始日志
        if (current_level == 2):
            print('-' * 8 + current_name)
        elif (current_level == 3):
            print('-' * 4 + current_name)
        #封装数据
        tarObj = NbsRegionDTO(current_code, parent_code, current_level,
                              current_name, current_town_country_code)
        tar_obj_set.add(tarObj)
        # 递归调用，获取下级数据
        tar_obj_set_result = set()
        if (current_level != 5 and current_url != ''):  # 五级一定没有下级
            # 当前解析页面截取最后一个'/'之前的url ，再拼接当前页面的href   就是下一级别的解析url
            pos = to_parse_url.rfind("/")
            next_url_data = to_parse_url[:pos] + '/' + current_url
            tar_obj_set_result = cycleSpider(current_code, current_level,
                                             next_url_data, error_data_set)
        # 合并两个集合结果集【取并集】 并返回
        tar_obj_set = tar_obj_set | tar_obj_set_result

    if (current_level == 2 or current_level == 3):
        time.sleep(10)
    return tar_obj_set
