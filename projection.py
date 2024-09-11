from osgeo import gdal, osr

if __name__ == '__main__':
    raster_ds = gdal.Open("H:/layers/buildings/campus_12.tiff")

    raster_type = raster_ds.GetRasterBand(1).DataType
    a = raster_ds.GetProjection()
    b = raster_ds.GetGeoTransform()
    b[1],b[5]
    gdal.Warp("H:/layers/campus_12n.tiff",raster_ds,dstSRS="EPSG:4326",width="2304",height="2304")
    raster = gdal.Open("H:/layers/campus_12n.tiff")
    a1 = raster_ds.GetProjection()
    # # 栅格投影
    # spatialRef = osr.SpatialReference()
    # spatialRef.ImportFromWkt(raster_ds.GetProjection())
    print(" ")