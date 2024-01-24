import math
import random
import time
import urllib.request as request
import os
from PIL import Image
import cv2
import numpy as np
from osgeo import gdal
from math import log, tan, radians, cos, pi, sinh, atan, degrees, pow

import pandas as pd

# ---------- CONFIGURATION -----------#
zoom = 17


def x_to_lon_edges(x, z):
    tile_count = pow(2, z)
    unit = 360 / tile_count
    lon = -180 + x * unit
    return lon


def y_to_lat_edges(y, z):
    tile_count = pow(2, z)
    unit = 1 / tile_count
    relative_y1 = y * unit
    lat = degrees(atan(sinh(pi * (1 - 2 * relative_y1))))

    return lat


def tile_edges(x, y, z, n):
    lat1 = y_to_lat_edges(y - n, z)
    lat2 = y_to_lat_edges(y + n + 1, z)
    lon1 = x_to_lon_edges(x - n, z)
    lon2 = x_to_lon_edges(x + n + 1, z)
    return [lon1, lat1, lon2, lat2]


def divideImg(out_dir, name, in_path, hsv_domain):
    pathN = np.empty(shape=(4, (n * 2 + 1) * (n * 2 + 1))).astype(object)  # 导出的路径


    for i in range(len(in_path)):

        src = cv2.imread(in_path[i])  # 原瓦片路径
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)  # BGR转HSV
        #  前三个
        num = 0
        for low_hsv, high_hsv in hsv_domain:
            path1 = out_dir[num] + name + '_{}.png'.format(i)
            # if not os.path.exists(path1):
            mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)  # 提取掩膜
            cv2.imwrite(path1, mask)
            #
            pathN[num][i] = path1
            num += 1

        # 第四个，道路部分 num = 3

        path2 = out_dir[num] + name + '_{}.png'.format(i)
        if not os.path.exists(path2):
            mask = cv2.inRange(hsv, lowerb=np.array([0, 80, 80]),
                               upperb=np.array([130, 255, 255]))  # 提取紫色h=0~30、黄、橙道路，主要道路
            gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)  # 转为灰度图
            ret, gray = cv2.threshold(gray, 251, 255, cv2.THRESH_BINARY_INV)  # 提取次要道路
            gray_contrary = 255 - gray
            mask_img = cv2.add(src, np.zeros(np.shape(src), dtype=np.uint8), mask=gray_contrary + mask)
            cv2.imwrite(path2, mask_img)
        pathN[num][i] = path2

    return pathN


def sec(x):
    return (1 / cos(x))


def latlon_to_xyz(lat, lon):
    tile_count = pow(2, zoom)
    x = (lon + 180) / 360
    y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
    return math.floor(tile_count * x), math.floor(tile_count * y)


def download_tile(x, y, tile_server, path, n):
    num = 0
    path_out = []

    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            name = path + '_' + str(num) + '.png'
            # if not os.path.exists(name):
            url = tile_server.replace(
                "{x}", str(x + j)).replace(
                "{y}", str(y + i)).replace(
                "{z}", str(zoom))
            request.urlretrieve(url, name)
                # time.sleep(random.uniform(2, 5))
            num += 1
            path_out.append(name)

    return path_out


def image_compose(n, image_save_path, image_dir):
    col = 2 * n + 1
    image_size = 256
    to_image = Image.new('RGBA', (col * image_size, col * image_size))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    num = 0
    for y in range(col):
        for x in range(col):
            from_image = Image.open(image_dir[num])
            to_image.paste(from_image, (x * image_size, y * image_size))
            num += 1
    return to_image.save(image_save_path)  # 保存新图


if __name__ == '__main__':
    keys = ["e03b90d8b3e27a8c02ff84647f722afa", "01ded7f9fb2887ebb205123ba776c10b", "4de94f67a6ff239191334cadbd483e37",
            "713b143ef7f4718372ef0e8dc2a5ea13", "4d332f3ba0db88a7e956a93068f13a37"]

    tile_server = "http://t0.tianditu.gov.cn/vec_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE" \
                  "=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk="
    tile_server_img = "http://t0.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE" \
                      "=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk="

    path = 'H:/png/'  # 总文件夹
    n = 4  # 向左四格，向右四格

    data = pd.read_csv('forChina/AOI_all_N.csv')  # 表格
    type01 = ['vec', 'img', 'river', 'green', 'buildings', 'road']  # 六个文件夹

    hsv_domain = [[np.array([100, 20, 220]), np.array([110, 255, 255])],
                  [np.array([61, 20, 207]), np.array([100, 255, 255])],
                  [np.array([33, 0, 249]), np.array([35, 8, 255])]]  # 色彩范围。 river, green, buildings

    dir_path = []
    # 分别新建文件夹
    for t in type01:
        dir_path.append(path + t + '/')
        if not os.path.exists(path + t):
            os.mkdir(path + t)
    for t in type01:
        if not os.path.exists("H:/layers/" + t + '/'):
            os.mkdir("H:/layers/" + t + '/')

    for i in {6,61,161,237,357,433,1259,1260,1261,1262}:  # 对每一个学校
        # 读取经纬度+ FID
        fid = data['FID'][i]
        lat = data['latC'][i]
        lon = data['lngC'][i]
        x, y = latlon_to_xyz(lat, lon)  # 计算行列数
        campus_name = 'campus_{}'.format(fid)
        # keyN = random.randint(0,4)
        keyN = 0
        # step 1 下载瓦片,如果已有不会重复下载，仅制作路径
        # print(tile_server + keys[keyN])
        vec_path = download_tile(x, y, tile_server + keys[keyN], dir_path[0] + campus_name, n)  # 下载瓦片
        img_path = download_tile(x, y, tile_server_img + keys[keyN], dir_path[1] + campus_name, n)  # 下载瓦片

        path01 = np.array([vec_path, img_path])

        # step3 将地图瓦片，按颜色分割成多张，4，如果已有不会重复处理
        path02 = divideImg(dir_path[2:], campus_name, vec_path, hsv_domain)  # 输入vec_path
        path_all = np.concatenate((path01, path02))

        # step4 为每张增加坐标信息
        bounds = tile_edges(x, y, zoom, n)
        # step 2 合成一张图

        for p in range(len(path_all)):
            path_out = "H:/layers/" + type01[p] + '/' + campus_name + '.png'
            # if not os.path.exists(path_out):
            image_compose(n, path_out, path_all[p])

            path_out_tiff = path_out.replace('png', 'tiff')
            # if not os.path.exists(path_out_tiff):
            gdal.Translate(path_out_tiff,
                           path_out,
                           outputSRS='EPSG:4326',
                           outputBounds=bounds,options=["COMPRESS=LSW"])

        print(campus_name + ' is done')
        time.sleep(random.uniform(5, 15))
