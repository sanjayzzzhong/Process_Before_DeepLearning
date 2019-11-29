# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-08-22 13:15:03
'''
import cv2


path = "/home/sanjay/DATA/Project_Datasets/1_City_Project/collect/manh/manhole/full_1/IMG_20190808_134443.jpg"

img = cv2.imread(path)
cv2.imshow("test", img)
cv2.waitKey(0)
# cv2.imwrite()