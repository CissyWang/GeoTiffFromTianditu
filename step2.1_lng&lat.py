import pandas as pd


# 取出表格内的经纬度用于转换

def extractLng_Lat(data, export_path):
    # data = pd.read_csv(path)
    # print(data)
    # print(data.loc[1, 'geo_lng'])
    final = pd.DataFrame(columns=('num', 'lng', 'lat'))
    for i in range(len(data)):

        final.at[i, 'num'] = i + 1
        # print(data.at[i, 'geo_lng'])
        try:
            final.at[i, 'lng'] = data.loc[i, 'lng']
            final.at[i, 'lat'] = data.loc[i, 'lat']
        except KeyError:
            print('cannot found lng&lat')
            break

    final.to_csv(export_path, header=False, index=False)


def combine_LngLat_toNew(data, path_new, export_path):
    # data = pd.read_csv(path)
    data_new = pd.read_csv(path_new, header=None)
    # print(data_new.loc[1, 'geo_lng'])
    for i in range(len(data)):
        # print(data_new.iloc[i, 1])
        data.at[i, 'lngN'] = data_new.iloc[i, 1]
        data.at[i, 'latN'] = data_new.iloc[i, 2]

    data.to_csv(export_path, header=True, index=False)


if __name__ == '__main__':
    path = 'getAOIsim.csv'
    data = pd.read_csv(path)

    # 取出lng，lat列
    # export_path = 'lng&lat_' + path
    # extractLng_Lat(data, export_path)

    # 把转化后的合并
    export_path1 = 'trans1_' + path
    path_new = 'Trans_xy.csv'
    combine_LngLat_toNew(data, path_new, export_path1)
