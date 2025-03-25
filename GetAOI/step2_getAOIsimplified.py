
"""
获得AOI不需要 api是一个网页。
但坐标转化需要key，日限额4000
-1=没有AOI,0=未爬取或未转化成功,1=爬取成功
可以多运行几次把 0 的全部爬取完
爬取后，用step2.1 转换坐标为WGS48
"""

import csv
import re
import pandas as pd
import requests
import time  # 控制时间暂停
import random  # 产生随机数
import json
import step1_getPOIfromNameNew as step1  # 调用第一步的headers 和 key

"""将列表坐标处理为','和';'间隔的字符串
返回米制坐标转经纬度链接:
http://api.map.baidu.com/geoconv/v1/?coords=114.21892734521,29.575429778924&from=6&to=5&ak=sfW*************ACnzp
自定义函数：AK改为自己的,多个坐标用‘；’间隔
"""


def bdTrans(geo, headers):
    keyN = random.randint(0, len(step1.key) - 1)
    key = step1.key[keyN]
    num = int((len(geo) - 1) / 2)
    dd = []
    for i in range(0, num, 20):
        geox = ''
        if i + 20 < num:
            j = i + 20
        else:
            j = num
        for n in range(i, j):
            tx = str(geo[2 * n]) + ',' + str(geo[2 * n + 1])
            geox = geox + ';' + tx
        # 百度坐标转换API， 6百度坐标，5 百度bd09经纬度坐标.现在一次只能转10个
        bdzb_url = 'http://api.map.baidu.com/geoconv/v1/?coords=' + geox.lstrip(
            ';') + '&from=6&to=5&ak=' + key
        # bdzb_url = 'http://api.map.baidu.com/geoconv/v1/?coords=' + geox.lstrip(
        #     ';') + '&from=6&to=1&ak=w9HGFgmL64By3EbCf8ukfEIwx4uCqHjk'
        zb_data_wb = requests.get(bdzb_url, headers=headers)  # 根据经纬度获取信息
        zb_data = json.loads(zb_data_wb.text)
        # print(type(zb_data['result']))
        dd += zb_data['result']
    return dd


def getAOIpoints(i, poi):
    url = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&ext_ver=new&l=12&uid=' + poi.loc[i, 'uid']
    wb_data = requests.get(url, headers=step1.headers)  # 获取信息
    data = json.loads(wb_data.text)
    if 'geo' not in data['content']:  # 不存在AOI ？？
        poi.loc[i, 'get'] = -1
        print(str(poi.loc[i, 'num']) + ',' + str(poi.loc[i, 'campusName'] + ',-1'))
        return

    num0 = data['content']['geo']
    try:
        # num00 = num0.split('|')[1].replace(',', ';')
        num01 = num0.split('|1-')[1].replace(',', ';')
        geo = num01.split(';')
        # 获取边界需要的 url
        dd = bdTrans(geo, step1.headers)
        # 获取每个点对应的边界的结果 dd

        # 写入每个点对应的边界点的行
        for j in range(len(dd)):
            writer.writerow([poi.at[i, 'num'], poi.at[i, '序号'], poi.at[i, '学校标识码'], poi.at[i, 'uid'],
                             dd[j]['x'], dd[j]['y'], str(j + 1)])

        print(str(poi.loc[i, 'num']) + ',' + str(poi.loc[i, 'campusName']))
        poi.loc[i, 'get'] = 1
        f.flush()


    except:  # 转换失败
        # writer.writerow([poi.at[i, 'num'], poi.at[i, '序号'], poi.at[i, '学校标识码'], poi.at[i, 'uid'],
        #                  'x', 'y', str(0)])
        print(str(poi.loc[i, 'num']) + ',' + str(poi.loc[i, 'campusName'] + ',x'))
    time.sleep(random.uniform(1.0, 5.0))  # 随机休眠


if __name__ == '__main__':
    inputP = 'forChina/1.2_poi_college_Baidu_S.csv'
    outputP = 'forChina/2_getAOI_college.csv'

    # 输入表格
    poi = pd.read_csv(inputP)  # ID信息

    # 如果第一次爬
    if 'get' not in poi.columns:
        poi['get'] = 0
        # 创建表头
        final = pd.DataFrame(
            columns=('num',
                     '序号', 'campusID', 'uid',
                     'geo_lng', 'geo_lat', 'order'))
        final.to_csv(outputP, index=False)

    # 否则
    f = open(outputP, 'a', encoding='utf-8', newline='')
    writer = csv.writer(f)
    try:
        for i in range(3, len(poi)):
            if poi.loc[i, 'get'] != 0:
                continue
            getAOIpoints(i, poi)
            # url = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&ext_ver=new&l=12&uid=' + poi.loc[i, 'uid']
            # wb_data = requests.get(url, headers=headers)  # 获取信息
            # data = json.loads(wb_data.text)
            # # 利用uid获取百度地图的对应AOI数据
            #
            # try:
            #     num0 = data['content']['geo']
            #     # num00 = num0.split('|')[1].replace(',', ';')
            #     num01 = num0.split('|1-')[1].replace(',', ';')
            #     geo = num01.split(';')
            #     # 获取边界需要的 url
            #     dd = bdTrans(geo, headers)
            #     # 获取每个点对应的边界的结果 dd
            #
            #     # 写入每个点对应的边界点的行
            #     for j in range(len(dd)):
            #         writer.writerow([poi.at[i, 'num'], poi.at[i, '序号'], poi.at[i, '学校标识码'], poi.at[i, 'uid'],
            #                          dd[j]['x'], dd[j]['y'], str(j + 1)])
            #
            #     print(str(poi.loc[i, 'num']) + ',' + str(poi.loc[i, 'campusName']))
            #     poi.loc[i, 'get'] = 1
            #
            # # 如果搜索不到结果
            # except:
            #     writer.writerow([poi.at[i, 'num'], poi.at[i, '序号'], poi.at[i, '学校标识码'], poi.at[i, 'uid'],
            #                      'x', 'y', str(0)])
            #     print(str(poi.loc[i, 'num']) + ',' + str(poi.loc[i, 'campusName'] + ',x'))
            #     f.flush()
            # time.sleep(random.uniform(1.0, 5.0))  # 随机休眠
    finally:
        # 保存数据
        f.close()
        poi.to_csv(inputP, index=False)

# 爬取AOI 简化后
# 爬取后，用step2.1 转换坐标为WGS48

import csv
import re
import pandas as pd
import requests
import time  # 控制时间暂停
import random  # 产生随机数
import json


# 将列表坐标处理位','和';'间隔的字符串
# 返回米制坐标转经纬度链接
# http://api.map.baidu.com/geoconv/v1/?coords=114.21892734521,29.575429778924&from=6&to=5&ak=sfW*************ACnzp

# 自定义函数：AK改为自己的,多个坐标用‘；’间隔
# 合成坐标转换申请链接：百度米制坐标转百度经纬度

def bdTrans(geo,headers):
    num = int((len(geo) - 1) / 2)
    dd = []
    for i in range(0,num,20):
        geox = ''
        if i+20<num:
            j = i+20
        else:
            j=num
        for n in range(i,j):
            tx = str(geo[2 * n]) + ',' + str(geo[2 * n + 1])
            geox = geox + ';' + tx
        # 百度坐标转换API， 6百度坐标，5 百度bd09经纬度坐标.现在一次只能转10个
        bdzb_url = 'http://api.map.baidu.com/geoconv/v1/?coords=' + geox.lstrip(
            ';') + '&from=6&to=5&ak=w9**************Hjk'
        # bdzb_url = 'http://api.map.baidu.com/geoconv/v1/?coords=' + geox.lstrip(
        #     ';') + '&from=6&to=1&ak=w9*************Hjk'
        zb_data_wb = requests.get(bdzb_url, headers=headers)  # 根据经纬度获取信息
        zb_data = json.loads(zb_data_wb.text)
        # print(type(zb_data['result']))
        dd += zb_data['result']
    return dd


# 合成url


if __name__ == '__main__':
    # 创建表头
    final = pd.DataFrame(
        columns=(
            'num','campusID', 'uid',
            'geo_lng', 'geo_lat','order'))
    final.to_csv('getAOI.csv')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

    # 输入表格
    txt = pd.read_csv('poi-BaiduS.csv')  # 小区ID信息
    # txt['geo'] = 'x'  # 增加geo列

    f = open('getAOI.csv', 'a', encoding='utf-8', newline='')
    writer = csv.writer(f)
    ###

    for i in range(len(txt)):
        url = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&ext_ver=new&l=12&uid=' + txt.loc[i, 'uid']
        wb_data = requests.get(url, headers=headers)  # 获取信息
        data = json.loads(wb_data.text)
        # 利用uid获取百度地图的对应AOI数据

        try:
            num0 = data['content']['geo']
            # num00 = num0.split('|')[1].replace(',', ';')
            num01 = num0.split('|1-')[1].replace(',', ';')
            geo = num01.split(';')
            # 获取边界需要的 url
            dd = bdTrans(geo,headers)
            # 获取每个点对应的边界的结果 dd
            print(len(dd))

            # 写入每个点对应的边界点的行
            for j in range(len(dd)):
                writer.writerow([txt.at[i, 'num'], txt.at[i, 'campusID'], txt.at[i, 'uid'],
                                 dd[j]['x'], dd[j]['y'], str(j + 1)])

            print(str(txt.loc[i, 'num']) + ',' + str(txt.loc[i, 'name']))

        # 如果搜索不到结果
        except:
            writer.writerow([txt.at[i, 'num'], txt.at[i, 'campusID'], txt.at[i, 'uid'],
                             'x', 'y', str(0)])
            print(str(txt.loc[i, 'num']) + ',' + str(txt.loc[i, 'name']+',x'))
            f.flush()
        time.sleep(random.uniform(1.0, 5.0))  # 随机休眠
    # 保存数据
    f.close()

