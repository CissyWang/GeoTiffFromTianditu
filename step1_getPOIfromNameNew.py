"""
framework: list-(search position API)->json contains 10 positions for each university
->campus POI -(url,meter to lon&lat)-> available campus POI+ boundary points-(bd To WGS48)
->points in WGS48 -(ArcGIS)-> face and point shapefile
->centerPoint ->tiles -> layers -> geotiff

百度地图API，用城市+类型+名称获取POI，日均限制100，超出有几率可获得
以下代码使用多个key交替，反复补齐缺失部分
获得结果存储json
"""

import json
import os.path

import pandas as pd
import requests
import time  # 控制时间暂停
import random  # 产生随机数
import re
import csv


# 合成百度API地址
def address_web(name, city, MyAK):
    query = 'query=' + name
    tag = 'tag=高等院校'
    region = 'region=' + city
    rawstr = query + '&' + tag + '&' + region + '&city_limit=true&page_size=10&output=json&ak='  # 一个学校搜出10个结果
    url = 'http://api.map.baidu.com/place/v2/search?' + rawstr + MyAK
    return url


def groupbyCity(path,output):
    # 读取名单按照城市排序
    poi = pd.read_csv(path)  # 读取名单
    dict1 = poi.groupby("所在地").size().sort_values(ascending=False).to_dict()
    poi["countOfCity"] = poi['所在地'].map(dict1)
    poi.sort_values(by=['countOfCity'], ascending=False)
    poi.reset_index(drop=True)
    poi.to_csv(output)
    return poi


def getJson(df, i, key):
    name = df.loc[i, '学校名称']
    city = df.loc[i, '所在地']
    url = address_web(name, city, key)
    try:
        wb_data = requests.get(url, headers=headers)  # 通过url和用户代理获取信息
        data = json.loads(wb_data.text)
    except:
        data = ''
    return data


def firstRequest(start, end, jsonPath, keys):
    for i in range(start, end):
        # 用于生成url
        keyN = random.randint(0, len(keys)-1)
        data = getJson(poi, i, keys[keyN])

        if data != '':
            # 把获取的内容存储一份json
            try:
                with open(jsonPath, 'r', encoding='utf-8') as json_file:
                    old_data = json.load(json_file)

                with open(jsonPath, 'w+', encoding='utf-8') as json_file:
                    old_data.append(data)
                    json_file.write(json.dumps(old_data, indent=True, ensure_ascii=False))  # indent 缩进
            except FileNotFoundError:  # 第一次，要创建
                with open(jsonPath, 'a', encoding='utf-8') as json_file:
                    old_data = json.dumps(data, indent=True, ensure_ascii=False)
                    json_file.write('[')
                    json_file.write(old_data)
                    json_file.write(']')  # indent 缩进
            except json.decoder.JSONDecodeError:
                break
                print('json文件有问题')

            print(i, poi.loc[i, '学校名称'])  # 成功的
            time.sleep(random.uniform(0.5, 2))  # 随机休眠
        else:
            print(i, poi.loc[i, '学校名称'], " not found")
            with open(jsonPath, 'w+', encoding='utf-8') as json_file:
                json_file.seek(-1, os.SEEK_END)
                json_file.truncate()
                json_file.write(',{}]')
            continue


def replace302(poi, json_path):
    file = open(json_path, 'r', encoding='utf-8')
    data = json.load(file)
    for i in range(0, len(data)):
        d = data[i]
        if d["status"] != 302:
            continue
        # 配额超出的部分
        keyN = random.randint(0, 3)
        new_data = getJson(poi, i, key[keyN])
        if (new_data == '') | (new_data['status'] == 302):
            continue

        data[i] = new_data  # 替换
        print(i, poi.loc[i, '学校名称'])
        with open(json_path, 'w+', encoding='utf-8') as json_file:
            json_file.write(json.dumps(data, indent=True, ensure_ascii=False))  # indent 缩进
        time.sleep(random.uniform(0.5, 2))


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
key = []
key.append('w9HGFgmL64By3EbCf8ukfEIwx4uCqHjk')  # 自行申请的百度AK
key.append('HFly4BCwoY2f3kjcuopCR1nbFrF3YMho')  # 自行申请的百度AK
key.append('GnLqcl4dCZltgWZ2XS1Aa9bystTGbsE0')
key.append('gaDCgieETZSoa2l8skP7jOM7sdPo89vp')

if __name__ == '__main__':

    # 若不存在按城市groupby的文件，则先groupby
    # if not os.path.exists('forChina/collegeSort.csv'):  # 'forChina/universitySort.csv'
    #     groupbyCity('forChina/chineseUniversity2021_college.csv')  # 'E:/greenland_Campus/UniversityInNanjing.csv'
    list = 'forChina/collegeSort.csv'
    try:
        poi = pd.read_csv(list)
    except FileNotFoundError:
        groupbyCity('forChina/chineseUniversity2021_college.csv',list)  # 'E:/greenland_Campus/UniversityInNanjing.csv'
        poi = pd.read_csv(list)

    jsonPath = 'forChina/college_poi1.json'

    # 第一遍爬取 获取json 超过配额的有概率获得不到
    firstRequest(0, len(poi), jsonPath, key)

    # 第二遍爬 把没得到的再补充一下
    #replace302(poi, jsonPath)
