from osgeo import gdal
from math import pi, sinh, atan, degrees


def x_to_lon_edges(x, z):
    tile_count = pow(2, z)
    unit = 360 / tile_count
    lon = -180 + x * unit
    lon1 = lon-3*unit
    lon2 = lon + 4*unit
    return(lon1, lon2)

def mercatorToLat(mercatorY):
    return (degrees(atan(sinh(mercatorY))))


def y_to_lat_edges(y, z):
    tile_count = pow(2, z)
    unit = 1 / tile_count
    relative_y1 = (y-3) * unit
    relative_y2 = (y+4)*unit
    lat1 = mercatorToLat(pi * (1 - 2 * relative_y1))
    lat2 = mercatorToLat(pi * (1 - 2 * relative_y2))
    return (lat1, lat2)

def tile_edges(x, y, z):
    lat1, lat2 = y_to_lat_edges(y, z)
    lon1, lon2 = x_to_lon_edges(x, z)
    return[lon1, lat1, lon2, lat2]

if __name__ == '__main__':

    bounds = tile_edges(108818, 53354,17)
    gdal.Translate('label123.tiff',
                   'label123.png',
                   outputSRS='EPSG:4326',
                   outputBounds=bounds)


#又平移又缩放
#     lon1,lat1,lon2,lat2 = tile_edges
#     gcp_items = [
#         [lon1, lat1, 0, 0],  # 左上，0行0列
#         [lon2, lat1, 1792, 0],  # 右上，0行x列
#         [lon1, lat2, 0, 1792],  # 左下，y行0列
#         [lon2, lat2, 1792, 1792]
#     ]
# #
#     gcp_list = []
#     for item in gcp_items:
#         x, y, pixel, line = item
#         z = 0
#         gcp = gdal.GCP(x, y, z, pixel, line)
#         gcp_list.append(gcp)
#
#     print(gcp_list)
#     options = gdal.TranslateOptions(format='GTiff', outputSRS='EPSG:4326', GCPs=gcp_list)
#     print(options)
#     gdal.Translate('OK21.tiff', 'test.png', options=options)
