import os
from PIL import Image
from osgeo import gdal
import cv2
import numpy as np
from osgeo import gdal

i = 12
input_shape = r"E:/greenland_Campus/GisDataforChina/AOI_All.shp"
aoi_path = "H:/layers/aoi/campus_{}.png".format(i)

# ds = gdal.Warp(aoi_path,
#                "H:/layers/buildings/campus_{}.tiff".format(i),
#                format='PNG',
#                width='2304',
#                height='2304',
#                cutlineDSName=input_shape,
#                cutlineWhere="FID = '{}'".format(i),
#                dstNodata='NULL', cropToCutline=False)  # 这里会改变图像高宽……

# 变成AOI二值图
# aoi = cv2.imread(aoi_path,cv2.IMREAD_UNCHANGED)
# b,g,r,a = cv2.split(aoi)
# cv2.imwrite(aoi_path,a)
# cv2.imshow("input", a)

cv2.namedWindow("input", cv2.WINDOW_AUTOSIZE)
src = cv2.imread("H:/layers/vec/campus_{}.png".format(i), )
mask1 = cv2.imread("H:/layers/river/campus_{}.png".format(i), cv2.IMREAD_GRAYSCALE)
mask2 = cv2.imread("H:/layers/green/campus_{}.png".format(i), cv2.IMREAD_GRAYSCALE)

hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
# mask3 = cv2.inRange(hsv, lowerb=np.array([0, 80, 80]),
#                    upperb=np.array([130, 255, 255]))  # 提取紫色h=0~30、黄、橙道路，主要道路
mask3 = cv2.imread("H:/layers/road/campus_{}.png".format(i), cv2.IMREAD_GRAYSCALE)
mask4 = cv2.imread("H:/layers/buildings/campus_{}.png".format(i), cv2.IMREAD_GRAYSCALE)

mask = cv2.imread(aoi_path, cv2.IMREAD_GRAYSCALE)
mask_inversed = cv2.bitwise_not(mask)

img = cv2.add(src, np.zeros(np.shape(src), dtype=np.uint8), mask=mask1 + mask2 + mask3 + mask4)
img_inside = cv2.add(img, np.zeros(np.shape(src), dtype=np.uint8), mask=mask)
img_outside = cv2.add(img, np.zeros(np.shape(src), dtype=np.uint8), mask=mask_inversed)

img_outside = cv2.resize(img_outside, (256, 256))  # 内部所有
cv2.imshow("input", img_outside) # 外部所有
# print(type(img))

cv2.waitKey(0)
cv2.destroyAllWindows()
