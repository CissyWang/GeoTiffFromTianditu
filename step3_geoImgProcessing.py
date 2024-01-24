import math
import random
import time
import urllib.request
import os
from PIL import Image
import cv2
import numpy as np
from osgeo import gdal
from math import log, tan, radians, cos, pi, sinh, atan, degrees
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


def divideImg(path, name, type, hsv_domain):
    pathN = []  # 导出的路径
    src = cv2.imread(path + 'vec_full/' + name)
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)  # BGR转HSV

    num = 0
    for low_hsv, high_hsv in hsv_domain:
        mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)  # 提取掩膜

        path1 = path + type[num] + '/' + name
        cv2.imwrite(path1, mask)
        pathN.append(path1)
        num += 1

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 251, 255, cv2.THRESH_BINARY_INV)
    path2 = path + type[num] + '/' + name
    pathN.append(path2)
    cv2.imwrite(path2, gray)
    return pathN


def sec(x):
    return (1 / cos(x))


def latlon_to_xyz(lat, lon):
    tile_count = pow(2, zoom)
    x = (lon + 180) / 360
    y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
    return math.floor(tile_count * x), math.floor(tile_count * y)


def download_tile(x, y, tile_server, path1, n):
    num = 0
    path11 = []

    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            url = tile_server.replace(
                "{x}", str(x + j)).replace(
                "{y}", str(y + i)).replace(
                "{z}", str(zoom))

            name = path1 + '/' + str(num) + '.png'
            urllib.request.urlretrieve(url, name)
            num += 1
            path11.append(name)
    return path11


def image_compose(n, image_save_path, image_dir):
    col = 2 * n + 1
    image_size = 256
    to_image = Image.new('RGBA', (col * image_size, col * image_size))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(col):
        for x in range(col):
            from_image = Image.open(image_dir + '/' + str(col * y + x) + '.png')
            to_image.paste(from_image, (x * image_size, y * image_size))
    return to_image.save(image_save_path)  # 保存新图


if __name__ == '__main__':
    tk = "e03b90d8b3e27a8c02ff84647f722afa"
    tile_server = "http://t0.tianditu.gov.cn/vec_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE" \
                  "=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=" + tk
    tile_server_img = "http://t0.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE" \
                      "=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=" + tk

    path = 'layers/'  # 总文件夹
    n = 4  # 向左四格，向右四格
    # 读取经纬度+ FID
    # lon = 118.95345
    # lat = 32.121552
    # fid = 1

    data = pd.read_csv('campus_select.csv')
    type01 = ['river', 'green', 'buildings', 'road']  # 四个文件夹
    hsv_domain = [[np.array([100, 20, 220]), np.array([110, 255, 255])],
                  [np.array([61, 20, 207]), np.array([100, 255, 255])],
                  [np.array([33, 0, 249]), np.array([35, 8, 255])]]
    for t in type01:
        if not os.path.exists(path + t):
            os.mkdir(path + t)
    if not os.path.exists(path + 'vec_full'):
        os.mkdir(path + 'vec_full')
    if not os.path.exists(path + 'img_full'):
        os.mkdir(path + 'img_full')

    for i in range(4, len(data)):
        fid = data['FID'][i]
        lat = data['latN'][i]
        lon = data['lngN'][i]
        x, y = latlon_to_xyz(lat, lon)  # 计算行列数
        final_name = 'campus_{}_{}_{}_{}.png'.format(fid, x, y, zoom)
        final_name_img = 'campus_{}_{}_{}_{}_img.png'.format(fid, x, y, zoom)

        # step 1 下载瓦片
        dir_path = path + 'campus_{}_{}_{}_{}'.format(fid, x, y, zoom)  # 单个文件夹
        dir_path_img = path + 'img_campus_{}_{}_{}_{}'.format(fid, x, y, zoom)  # 单个文件夹

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)  # 新建文件夹
        if not os.path.exists(dir_path_img):
            os.mkdir(dir_path_img)  # 新建文件夹
        download_tile(x, y, tile_server, dir_path, n)  # 下载瓦片
        download_tile(x, y, tile_server_img, dir_path_img, n)  # 下载瓦片

        # step 2 合成一张图
        image_compose(4, path + 'vec_full/' + final_name, dir_path)
        image_compose(4, path + 'img_full/' + final_name_img, dir_path_img)

        #  step3 一张图按颜色分割成多张，4
        path01 = divideImg(path, final_name, type01, hsv_domain)

        # step4 为每张增加坐标信息
        path01.append(path + 'vec_full/' + final_name)
        path01.append(path + 'img_full/' + final_name_img)
        bounds = tile_edges(x, y, zoom, n)  # 边界
        for p in path01:
            path_out = p.replace('png', 'tiff')
            gdal.Translate(path_out,
                           p,
                           outputSRS='EPSG:4326',
                           outputBounds=bounds)
            os.remove(p)
        print(final_name + ' is done')
        time.sleep(random.uniform(0, 5))
