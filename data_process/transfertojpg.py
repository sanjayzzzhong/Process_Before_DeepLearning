# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-13
'''
import os
import cv2
import sys
from PIL import Image

path = "/home/sanjay/DATA/Project_Datasets/2_Tibet_Project/1_Gun/gun_classify/img/"
new_path = "/home/sanjay/DATA/Project_Datasets/2_Tibet_Project/1_Gun/gun_classify/new_img/"
i = 1
for filename in os.listdir(path):
    if os.path.splitext(filename)[1] == ".jpg" or os.path.splitext(filename)[1] == ".png" or os.path.splitext(filename)[1] == ".JPEG" or os.path.splitext(filename)[1] == ".JPG" or os.path.splitext(filename)[1] == ".jpeg":
        try:
            img = Image.open(os.path.join(path, filename))

            ###########use cv2########
            #cv_img = cv2.imread(os.path.join(path, filename))
            ####################################
            # cv2.imshow("test", cv_img)
            # cv2.waitKey(0)
            # print(filename.replace(".jpeg", ".jpg"))
            # newfilename = "0000" + str(i) + ".jpg"
            # not rename first
            newfilename = os.path.splitext(filename)[0] + '.jpg'
            # newfilename = "muck_" + str(i) + ".jpg"
            img.save(os.path.join(new_path, newfilename))
            print(os.path.join(new_path, newfilename))

            ###########use cv.imwrite###############
            #cv2.imwrite(os.path.join(new_path, newfilename), cv_img)
            i = i + 1
            print(i)
        # 如果读取文件错误啥的就把这个文件删了吧
        except Exception as e:
            print("{} is broken, deleted!".format(filename))
            print(e)
            os.remove(os.path.join(path, filename)) # not delete yet
print("Totally transfer %d images" % i)
