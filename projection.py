from osgeo import gdal, osr



def raster_WGS2UTM(raster_path, UTM_raster_path, longitude, is_north):
    raster_ds = gdal.Open(raster_path)
    raster_type = raster_ds.GetRasterBand(1).DataType
    # 栅格投影
    spatialRef = osr.SpatialReference()
    spatialRef.ImportFromWkt(raster_ds.GetProjection())

    # 根据经度计算UTM区号,进而定义UTM投影
    zone = str(int(longitude/6) + 31)
    zone = int('326' + zone) if is_north else int('327' + zone)
    UTM_spatialRef = osr.SpatialReference()
    UTM_spatialRef.ImportFromEPSG(zone)

    # 投影转换
    coordinate_transfor = osr.CoordinateTransformation(spatialRef, UTM_spatialRef)

    # 仿射矩阵六参数
    geotransform = raster_ds.GetGeoTransform()

    # 左上角upper left、右下角lower right坐标
    ul_x = geotransform[0]
    ul_y = geotransform[3]
    lr_x = geotransform[0]+geotransform[1]*raster_ds.RasterXSize+geotransform[2]*raster_ds.RasterYSize
    lr_y = geotransform[3]+geotransform[4]*raster_ds.RasterYSize+geotransform[5]*raster_ds.RasterYSize

    # 左上角、右下角在目标投影中的坐标
    (UTM_ul_x, UTM_ul_y, UTM_ul_z) = coordinate_transfor.TransformPoint(ul_y, ul_x)
    (UTM_lr_x, UTM_lr_y, UTM_lr_z) = coordinate_transfor.TransformPoint(lr_y, lr_x)

    # 创建目标图像文件
    driver = gdal.GetDriverByName("GTiff")
    UTM_raster_ds = driver.Create(UTM_raster_path,
                                  raster_ds.RasterXSize,
                                  raster_ds.RasterYSize,
                                  raster_ds.RasterCount,
                                  raster_type)
    # 转换后图像的分辨率
    resolution = (UTM_lr_x-UTM_ul_x)/raster_ds.RasterXSize
    # 转换后图像的六个放射变换参数
    UTM_transform = [UTM_ul_x, resolution, 0, UTM_ul_y, 0, -resolution]
    UTM_raster_ds.SetGeoTransform(UTM_transform)
    UTM_raster_ds.SetProjection(UTM_spatialRef.ExportToWkt())
    # 投影转换后需要做重采样
    gdal.ReprojectImage(raster_ds, UTM_raster_ds, spatialRef.ExportToWkt(),
                        UTM_spatialRef.ExportToWkt(), gdal.GRA_Bilinear)
    # 关闭
    raster_ds = None
    UTM_raster_ds= None

if __name__ == '__main__':
    raster_WGS2UTM(r"H:/layers/buildings/campus_0.tiff", r"H:/layers/campusQ_0.tiff", 109.5, True)