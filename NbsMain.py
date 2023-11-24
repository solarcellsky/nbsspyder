import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from Bean.NbsRegionDTO import NbsRegionDTO
from NbsCycleSpider import cycleSpider
from SaveData import nbsDataToSaveBatch
from Util.UrlGetUtil import UrlGetUtil
'''国家统计局省级区域数据爬取 程序入口'''
base_url = 'http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/'
urlGetUtilObj = UrlGetUtil()
#两种方式二选一来爬取url页面
#urlopern方式
html = urlGetUtilObj.getByUrlOpen(base_url, 'gbk')
# request.get 方式
#html = urlGetUtilObj.getByRequestGet(base_url,'gbk')
'''
异常：Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER.
https://www.cnblogs.com/HANYI7399/p/6080070.html
'''
#bs = BeautifulSoup(html, 'html.parser', from_encoding = "iso-8859-1")
bs = BeautifulSoup(html, 'html.parser')
#找出存放省信息的tr行
trs = bs.findAll('tr', {'class': 'provincetr'})
#先取出所有的省数据节点
data_item_set = set()
for tr in trs:
    tds = tr.findAll('td')
    for td in tds:
        a_flag = td.a
        if a_flag is None:
            continue
        data_item_set.add(a_flag)

#全局变量，存储爬取过程中出现错误的数据
error_data_set = set()
# 每一轮节点的循环都是对一个省的数据处理
for a_flag in data_item_set:
    # 本省所有行政区划结果集
    tar_obj_set = set()
    #解析数据
    province_name = a_flag.get_text()  # 获取省名称
    print('-' * 12 + province_name + '---爬取开始' + '-' * 12)
    province_code = ''
    to_spider_url = a_flag['href']
    if len(province_name) == 0:
        continue
    if len(to_spider_url) != 0:
        province_code = ''.join(filter(str.isdigit,
                                       to_spider_url))  #列表转字符串，获取省一级code
    # 省一级数据封装成实体
    tarObj = NbsRegionDTO(province_code, '', 1, province_name, '')
    grade_2_url = base_url + to_spider_url  #基础路径拼接当前路径 相当于 下一级的url解析路径
    tar_obj_set.add(tarObj)
    #调用循环方法，去解析子层级区域
    tar_obj_set_result = cycleSpider(province_code, 1, grade_2_url,
                                     error_data_set)
    # 合并两个集合结果集【取并集】
    tar_obj_set = tar_obj_set | tar_obj_set_result
    print('-' * 12 + province_name + '---爬取结束' + '-' * 12)
    time.sleep(10)
    #本省数据入库存储
    try:
        nbsDataToSaveBatch(tar_obj_set)
    except Exception as e:
        print('-' * 12 + province_name + '---数据入库存储异常')
        print(e)

#全国数据初次处理完毕，开始处理整体过程中失败的数据，重试
print('------开始处理初次全国爬取失败的数据，共------' + str(len(error_data_set)) + '条')
while (len(error_data_set) > 0):
    error_data_set_second = set()
    for item in error_data_set:
        tar_save_set = cycleSpider(item.parent_code, item.parent_level,
                                   item.to_parse_url, error_data_set_second)
        #存储入库
        try:
            nbsDataToSaveBatch(tar_save_set)
        except Exception as e:
            print('---全国爬取过程的错误数据重试爬取后入库存储异常,---')
            print(e)
            for item in tar_save_set:
                print(item.nbs_code + '-' * 6 + item.nbs_parent_code +
                      '-' * 6 + str(item.nbs_level) + '-' * 6 + item.nbs_name +
                      '-' * 6 + item.nbs_town_country_code)

    #更新error_data_set
    print('------再次失败的数据，共------' + str(len(error_data_set_second)) + '条')
    error_data_set = error_data_set_second
    time.sleep(10)
