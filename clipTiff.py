import os
from PIL import Image
from osgeo import gdal



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
    input_shape = r"E:/greenland_Campus/GisDataforChina/AOI_All.shp"
    if not os.path.exists(dir):
        os.mkdir(dir)

    type01 = ['river']#, 'green', 'buildings', 'road'

    for i in range(0,1):
        for t in type01:

            # tif输入路径，打开文件
            # input_raster = r"H:/layers/{}/campus_{}.tiff".format(t,i)
            input_raster = r"H:/layers/campusQ_0.tiff".format(t, i)

            output_raster = dir + '/{}_inside_scale/campus_'.format(t) + str(i) + '.tif'
            output_png = output_raster.replace('tif','png')
            output_raster2 = dir + '/{}_inside/campus_'.format(t) + str(i) + '.tif'
            output_png2 = output_raster2.replace('tif','png')

            # if os.path.exists(output_raster):
            #     continue

            # 矢量文件路径，打开矢量文件
            input_raster = gdal.Open(input_raster)
            # 开始裁剪
            ds = gdal.Warp(output_raster,
                           input_raster,
                           format='GTiff',
                           cutlineDSName=input_shape,
                           cutlineWhere="FID = '{}'".format(i),
                           dstNodata='NULL', cropToCutline=True,
                           )
            ds2 = gdal.Warp(output_raster2,
                            input_raster,
                            format='GTiff',
                            cutlineDSName=input_shape,
                            cutlineWhere="FID = '{}'".format(i),
                            dstNodata='NULL', cropToCutline=False,
                            ) #  cropToCutline = True 裁剪到范围大小 dstSRS ='WGS_1984_UTM_Zone_50N'

            driver = gdal.GetDriverByName('GTiff')
            driver.CreateCopy(output_png, ds, strict=1, options=["TILED=YES", "COMPRESS=LZW"])
            driver.CreateCopy(output_png2, ds2, strict=1, options=["TILED=YES", "COMPRESS=LZW"])

            img = Image.open(output_png)
            img2 = Image.open(output_png2)

            image_data =toSqureJpg(img)
            image_data =image_data.resize((256, 256))  # 缩放
            image_data.save(output_raster.replace('tif', 'jpg'))

            image_data =toSqureJpg(img2)
            image_data.save(output_raster2.replace('tif','jpg'))

            os.remove(output_png)
            os.remove(output_png2)

        print(str(i)+" is done")

