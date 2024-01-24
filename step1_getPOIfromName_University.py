# 百度

import json
import pandas as pd
import requests
import time  # 控制时间暂停
import random  # 产生随机数
import re


# 合成百度API地址
def address_web(name):
    # MyAK = 'w9HGFgmL64By3EbCf8ukfEIwx4uCqHjk'  # 自行申请的百度AK
    MyAK = 'HFly4BCwoY2f3kjcuopCR1nbFrF3YMho'  # 自行申请的百度AK

    query = 'query=' + name
    tag = 'tag=高等院校'
    region = 'region=' + '南京市'
    rawstr = query + '&' + tag + '&' + region + '&city_limit=true&page_size=10&output=json&ak=' + MyAK  #一个学校搜出5个结果
    url = 'http://api.map.baidu.com/place/v2/search?' + rawstr

    return url


if __name__ == '__main__':

    # 创建一个带有表头的空文件
    final = pd.DataFrame(columns=('campusID','name', 'lng', 'lat', 'address', 'uid', 'city', 'district', 'type'))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

    poi = pd.read_csv(
        'E:/greenland_Campus/UniversityInNanjing.csv')  # 读取名单
    print(len(poi))
    # try:
    #     jsonfile = open("original.json",'x',encoding='utf-8',)
    # except:
    #     jsonfile = open("original.json", 'w', encoding='utf-8', )

    num=0
    for i in range(len(poi)):
        # 用于生成url
        name = poi.iloc[i, 1]
        city = '南京市'
        url = address_web(name)
        wb_data = requests.get(url, headers=headers)  # 通过url和用户代理获取信息
        data = json.loads(wb_data.text)

        # try:jsonfile.write(json.dumps(data['results']))
        # except:
        try:
            counts = len(data['results'])
            for j in range(counts):
                nameQ = data['results'][j]['name']
                reg = re.compile(r"^((%s)+(.(?!-).)*)" % name)
                mo = reg.match(nameQ)
                condition =(nameQ.endswith((")","学","区","院","校")))&(mo!=None)

                if condition:
                    final.at[num, 'name'] = nameQ
                    final.at[num, 'province'] = poi.iloc[i,4]
                    final.at[num, 'rank'] = poi.iloc[i,5]
                    final.at[num, 'type'] = poi.iloc[i,6]
                    final.at[num, 'campusID'] = poi.iloc[i, 2]

                    # 新表新增的列
                    final.at[num, 'lng'] = data['results'][j]['location']['lng']
                    final.at[num, 'lat'] = data['results'][j]['location']['lat']
                    final.at[num, 'address'] = data['results'][j]['address']
                    final.at[num, 'district'] = data['results'][j]['area']
                    final.at[num, 'uid'] = data['results'][j]['uid']
                    print(num, ',', nameQ,data['results'][j]['uid'])
                    num+=1
        except:
            print(num, '', name, ',', 'x')
            final.at[num, 'name'] = nameQ
            final.at[num, 'city'] = poi.iloc[i, 4]
            final.at[num, 'rank'] = poi.iloc[i, 5]
            final.at[num, 'type'] = poi.iloc[i, 6]
            final.at[num, 'campusID'] = poi.iloc[i, 2]

        time.sleep(random.uniform(0.5, 4))  # 随机休眠
    # jsonfile.close()
    final.to_csv('poi-Baidu3.csv', index=True, mode='a', header=False)





