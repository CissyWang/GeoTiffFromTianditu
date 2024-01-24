'''
测试发现拼起来比不拼要大很多
'''

from osgeo import gdal
from math import pi, sinh, atan, degrees
from PIL import Image

def x_to_lon_edges(x, z,n):
    tile_count = pow(2, z)
    unit = 360 / tile_count
    lon = -180 + x * unit
    lon1 = lon-(n-1)*unit
    lon2 = lon + n*unit
    return(lon1, lon2)

def mercatorToLat(mercatorY):
    return (degrees(atan(sinh(mercatorY))))


def y_to_lat_edges(y, z,n):
    tile_count = pow(2, z)
    unit = 1 / tile_count
    relative_y1 = (y-(n-1)) * unit
    relative_y2 = (y+n)*unit
    lat1 = mercatorToLat(pi * (1 - 2 * relative_y1))
    lat2 = mercatorToLat(pi * (1 - 2 * relative_y2))
    return (lat1, lat2)

def tile_edges(x, y, z,n):
    lat1, lat2 = y_to_lat_edges(y, z,n)
    lon1, lon2 = x_to_lon_edges(x, z,n)
    return[lon1, lat1, lon2, lat2]

def image_compose(n, image_save_path, image_dir):
    col = 2 * n + 1
    image_size = 256
    to_image = Image.new('RGBA', (col * image_size, col * image_size))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(col):
        for x in range(col):
            from_image = Image.open(image_dir + '/' + str(col * y + x) + '.tiff')
            to_image.paste(from_image, (x * image_size, y * image_size))
    return to_image.save(image_save_path)  # 保存新图
if __name__ == '__main__':

    bounds = tile_edges(108818, 53354,17,0)
    path = "campus_10_108817_53259_17"
    # for i in range(81):
    #     path1 = path+'/{}.tiff'.format(i)
    #
    #     gdal.Translate(path+'/{}.tiff'.format(i),
    #                    path+'/{}.png'.format(i),
    #                    outputSRS='EPSG:4326',
    #                    outputBounds=bounds)

    image_compose(4, path + '/vec_full.tiff', path)

