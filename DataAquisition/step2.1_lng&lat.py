import pandas as pd


# 取出表格内的经纬度用于转换

def extractLng_Lat(data, export_path):
    # data = pd.read_csv(path)
    # print(data)
    # print(data.loc[1, 'geo_lng'])
    final = pd.DataFrame(columns=('lng', 'lat'))

    final.index.name = 'num'
    final.index = final.index + 1
    # print(data.at[i, 'geo_lng'])
    try:
        final['lng'] = data['lng']
        final['lat'] = data['lat']
    except KeyError:
        print('cannot found lng&lat')

    final.to_csv(export_path, header=False)


def combine_LngLat_toNew(data, path_new, export_path):
    # data = pd.read_csv(path)
    data_new = pd.read_csv(path_new, header=None)
    # print(data_new.loc[1, 'geo_lng'])
    # for i in range(len(data)):
        # print(data_new.iloc[i, 1])
    data['lngN'] = data_new.iloc[:, 1]
    data['latN'] = data_new.iloc[:, 2]

    data.to_csv(export_path, header=True, index=False)


if __name__ == '__main__':
    path = 'forChina/2_poi_college_Baidu.csv'
    data = pd.read_csv(path)

    # 取出lng，lat列，方便用软件转换
    # export_path = 'org_xy.csv'
    # extractLng_Lat(data, export_path)

    # 把转化后的合并
    export_path1 = 'forChina/2.1_poi_college_Baidu_trans.csv'
    path_new = 'Trans_xy.csv'
    combine_LngLat_toNew(data, path_new, export_path1)


