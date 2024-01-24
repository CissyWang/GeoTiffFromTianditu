"""
这部分程序用于解析 step1 获得的json
需要配合校园名单使用
"""

import csv
import re
import pandas as pd
import json

"""判断是否是大学校区"""
def verifyCampus(name, nameOri):
    reg = re.compile(r"^((%s)+(.(?!-).)*)" % nameOri)
    mo = reg.match(name)
    condition = (name.endswith((")", "学", "区", "院", "校"))) & (mo != None)
    condition2 = name.endswith('医院') == False
    condition1 = len(re.findall('附属|-|中学|小学|公寓|科技园|家属', name)) == 0
    return condition & condition2 & condition1


if __name__ == '__main__':
    # 修改
    output_path = 'forChina/1.2_poi_college_Baidu.csv'  # 输出列表
    poi = pd.read_csv('forChina/1_collegeSort.csv')  # 原始列表
    file = open('forChina/college_poi1.json', 'r', encoding='utf-8')  # json列表

    data = json.load(file)  # json 每个学校十个

    with open(output_path, mode='w', encoding='utf-8', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["num", "uni_num", "序号", "学校名称", "学校标识码", "主管部门", "所在地", "办学层次", "备注", "campusName", "lng", "lat", "uid",
             "area"])

    campusIn = 0  # 校园的编号，一个大学有几个校园
    with open(output_path, mode='a', encoding='utf-8', newline="") as f:
        for i in range(len(data)):

            writer = csv.writer(f)
            listS = [s for s in poi.iloc[i, 0:-1]]  # 原始列表里的整行数据

            counts = len(data[i]["results"])
            if counts == 0:
                print('xxx,', i, poi.loc[i, '学校名称'])  # 没有数据
                continue

            campusCount = 0
            for j in range(counts):  # 每个数据
                dataR = data[i]["results"][j]

                nameQ = dataR['name']
                if verifyCampus(nameQ, poi.loc[i, '学校名称']):  # 如果名称符合要求
                    listA = [campusIn]  # 序号
                    listA.extend(listS)  # 原先的信息
                    listA.extend([nameQ, dataR['location']['lng'],
                                  dataR['location']['lat'], dataR['uid'],
                                  dataR['area']])  # 经纬度 uid 面积
                    writer.writerow(listA)  # 写入

                    print(campusIn, ',', i, nameQ, dataR['uid'])
                    campusIn += 1
                    campusCount += 1

            if campusCount == 0:
                print('xxx,', i, poi.loc[i, '学校名称'])  # 没有符合要求的
            else:
                f.flush()  # 刷新并释放缓冲区
