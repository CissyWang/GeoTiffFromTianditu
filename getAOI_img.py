import os
from PIL import Image
from osgeo import gdal
import cv2
import numpy as np
from osgeo import gdal


def toSqureJpg(image):
    image = image.convert('RGBA')
    w, h = image.size

    background = Image.new('RGB', size=(max(w, h), max(w, h)), color=(0, 0, 0))  # 创建背景图，颜色值为127
    length = int(abs(w - h) // 2)  # 一侧需要填充的长度
    box = (length, 0) if w < h else (0, length)  # 粘贴的位置
    background.paste(image, box, mask=image)
    return background


def getMask(input, outpath):
    aoi = cv2.imread(input, cv2.IMREAD_UNCHANGED)
    b, g, r, a = cv2.split(aoi)  # 提取掩膜
    cv2.imwrite(outpath, a)  # 用于后续切割的mask



if __name__ == '__main__':
    input_shape = r"E:/greenland_Campus/GisDataforChina/aoi_geo1.shp"
    for i in range(1263):
        aoi_path = "H:/layers/aoi/campus_{}.png".format(i)
        aoi_path1 = "H:/Clip/aoi/campus_{}.jpg".format(i)
        aoi_path_scale = "H:/Clip/aoi_scale/campus_{}.png".format(i)

        # AOImask.png 2304
        gdal.Warp(aoi_path,
                  "H:/layers/green/campus_{}.tiff",
                  format='PNG',
                  cutlineDSName=input_shape,
                  cutlineWhere="FID = '{}'".format(i),
                  dstNodata='NULL', cropToCutline=False, width="2304", height="2304")  # 这里会改变图像高宽……,dstSRS =""
        getMask(aoi_path, aoi_path)

        # 缩小的aoi.jpg
        img = Image.open(aoi_path)
        image_data = img.resize((256, 256))
        image_data.save(aoi_path1)  # 缩放的AOI

        # 缩放后的AOI
        #  获取mask
        getMask("H:/Clip/river_inside_scale/campus_{}.tif",aoi_path_scale)  # 中间文件png
        #  变成正方形并缩放
        img = Image.open(aoi_path_scale)
        image_data = toSqureJpg(img)
        image_data = image_data.resize((256, 256))  # 缩放
        image_data.save(aoi_path_scale.replace('png', 'jpg'))
        os.remove(aoi_path_scale)


