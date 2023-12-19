"""
  __author__=chatgpt、shadow
"""

import numpy as np
from PIL import Image
from osgeo import gdal, osr

# 加载 PNG 图像并获取图像数据 TODO 普通PNG图片
png_image = Image.open("test.png")
image_data = np.array(png_image)
height, width, channels = image_data.shape

# 定义 GeoTIFF 文件的输出路径和文件名 TODO GEOTIFF图片（带坐标的tif图片）
output_geotiff = "ok3.tiff"

# 创建 GeoTIFF 文件
driver = gdal.GetDriverByName("GTiff")
geotiff_dataset = driver.Create(output_geotiff, width, height, channels, gdal.GDT_Byte)

# 将 PNG 图像数据写入 GeoTIFF 文件
for band in range(channels):
    geotiff_band = geotiff_dataset.GetRasterBand(band + 1)
    geotiff_band.WriteArray(image_data[:, :, band])

# 定义 PNG 图像的边缘坐标（WSG84） TODO 依次 左上角、右上角、右下角坐标
top_left = (118.86932373046875, 31.71181291435097)
top_right = (118.8885498046875, 31.71181291435097)
bottom_right = (118.8885498046875, 31.69545579777871)

# 定义 GeoTIFF 文件的空间参考（Spatial Reference）
spatial_reference = osr.SpatialReference()
spatial_reference.ImportFromEPSG(4326)  # WGS84 EPSG code

# 设置 GeoTIFF 文件的地理转换信息（GeoTransform）
geotransform = (
    top_left[0], (top_right[0] - top_left[0]) / width, 0,
    top_left[1], 0, (bottom_right[1] - top_left[1]) / height
)

geotiff_dataset.SetGeoTransform(geotransform)
geotiff_dataset.SetProjection(spatial_reference.ExportToWkt())

# 设置 GeoTIFF 文件的重采样方法为最近邻法
geotiff_dataset.SetMetadataItem('RESAMPLING', 'NEAREST_NEIGHBOR')

# 设置 GeoTIFF 文件的压缩方法为 DEFLATE
geotiff_dataset.SetMetadataItem('COMPRESS', 'DEFLATE')

# 保存并关闭 GeoTIFF 文件
geotiff_dataset.FlushCache()
geotiff_dataset = None