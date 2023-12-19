import cv2
import numpy as np

src = cv2.imread(r"test2.png")  # 这里填你的原图像路径
# cv2.namedWindow("input", cv2.WINDOW_AUTOSIZE)
# cv2.imshow("input", src)


hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)  # BGR转HSV

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
ret, gray = cv2.threshold(gray, 251, 255, cv2.THRESH_BINARY_INV)
print(ret)

cv2.imshow("image", gray)

low_hsv = np.array([0, 0, 240])  # 这里要根据HSV表对应，填入三个min值（表在下面）
high_hsv = np.array([5, 255, 255])  # 这里填入三个max值
mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)  # 提取掩膜

# mask = cv2.medianBlur(mask, 3) #核尺寸是奇书
# 黑色背景转透明部分
# mask_contrary = mask.copy()
# mask_contrary[mask_contrary==0]=1
# mask_contrary[mask_contrary==255]=0#把黑色背景转白色
# mask_bool = mask_contrary.astype(bool)
# #这个是把掩模图和原图进行叠加，获得原图上掩模图位置的区域
# mask_img = cv2.add(src, np.zeros(np.shape(src), dtype=np.uint8), mask=mask)

# 这里如果背景本身就是白色，可以不需要这个操作，或者不需要转成透明背景就不需要这里的操作
# mask_img=cv2.cvtColor(mask_img,cv2.COLOR_BGR2BGRA)
# mask_img[mask_bool]=[0,0,0,0]


# cv2.imshow("image",mask)
# cv2.imwrite('label123.png',mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
