# GeoTiffFromTianditu
get map tile from Tiantidu and process, transfer to Geotiff which can be used in GIS map

## 1.GetAOI
- step1反复爬取获得全部POI的json文件
- step1.1 获得的json文件解析，按名称筛选，加入原csv列表？
- step2 利用poi对应的url，找到对应AOI的信息
- step 2.1 坐标转换，这部分尝试了一些转换代码，最后发现“万能坐标转换（未来交通实验室出品）”工具最准确，所以编写脚本提取出转换需要的格式+合成转换好的文件
## 2.GetImageData
- step 3 根据学校位置爬取地图瓦片，处理，保存完整和分层的GeoTif

