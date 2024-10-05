import os

from osgeo import gdal

type01 = ['vec', 'img','river', 'green', 'road', 'buildings']

for t in type01:
    for i in range(0, 1263):

        # tif输入路径
        input_file = r"H:/layers/{}/campus_{}.tiff".format(t, i)
        # 压缩后的路径
        path = r"H:/layers/{}_compressed/".format(t)

        if not os.path.exists(r"H:/layers/{}_compressed".format(t)):
            os.mkdir(path)

        output_file = path+r"campus_{}.tif".format(i)
        dataset = gdal.Open(input_file, gdal.GA_ReadOnly)

        driver = gdal.GetDriverByName('GTiff')
        options = ['COMPRESS=LZW', 'TILED=YES','BIGTIFF=YES']
        output_dataset = driver.CreateCopy(output_file, dataset, 0,options) #, options

        output_dataset.SetGeoTransform(dataset.GetGeoTransform())
        output_dataset.SetProjection(dataset.GetProjection())

dataset = None
output_dataset = None