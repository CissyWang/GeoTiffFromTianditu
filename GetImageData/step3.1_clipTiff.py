import os
from PIL import Image
from osgeo import gdal
'''
用AOI.shp 裁剪 GeoTif，并把结果输出为统一大小的方向png。
building_inside : scale
road inside: scale
landscape inside: scale

context:street+road
context:street + landscape
context: street+ buildings
'''

# 把裁剪后的图像缩放到统一大小的正方形中
def toSqureJpg(image):
    image = image.convert('RGBA')
    w, h = image.size

    background = Image.new('RGB', size=(max(w, h), max(w, h)), color=(127, 127, 127))  # 创建背景图，颜色值为127
    length = int(abs(w - h) // 2)  # 一侧需要填充的长度
    box = (length, 0) if w < h else (0, length)  # 粘贴的位置
    background.paste(image, box, mask=image)
    return background


if __name__ == '__main__':
    dir = r'H:/Clip'
    input_shape = r"E:/greenland_Campus/GisDataforChina/aoi_geo1.shp"  # should be WGS1948
    if not os.path.exists(dir):
        os.mkdir(dir)

    type01 = ['vec','river', 'green', 'road','buildings']

    for i in range(0,1263):
        for t in type01:

            # tif输入路径
            input_raster = r"H:/layers/{}/campus_{}.tiff".format(t, i)
            # 裁剪后的路径
            output_raster = dir + '/{}_inside_scale/campus_'.format(t) + str(i) + '.tif'
            output_png = output_raster.replace('tif','png')

            # if os.path.exists(output_raster):
            #     continue

            # 矢量文件路径，打开矢量文件
            input_raster = gdal.Open(input_raster)
            b = input_raster.GetGeoTransform() # 按照瓦片的投影坐标系

            # 开始裁剪，裁剪的这个没有坐标系？
            ds = gdal.Warp(output_raster,
                           input_raster,
                           format='GTiff',
                           cutlineDSName=input_shape,
                           cutlineWhere="FID = '{}'".format(i),
                           dstNodata='NULL', cropToCutline=True,xRes=b[1],yRes=b[5],
                           dstSRS=input_raster.GetProjection()
                           )

            # 制作像素图
            # driver = gdal.GetDriverByName('GTiff')
            # driver.CreateCopy(output_png, ds, strict=1, options=["TILED=YES", "COMPRESS=LZW"])
            #
            # img = Image.open(output_png)
            # image_data =toSqureJpg(img)  # 粘贴到方形
            # image_data =image_data.resize((256, 256))  # 缩放
            # image_data.save(output_raster.replace('tif', 'jpg'))
            #
            # os.remove(output_png)

        print(str(i)+" is done")

