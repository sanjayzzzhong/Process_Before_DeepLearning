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

path = "/home/sanjay/DATA/Project_Datasets/Tibet_Project/Knife/n03973628_img/"
new_path = "/home/sanjay/DATA/Project_Datasets/Tibet_Project/Knife/img/"
i = 1
for filename in os.listdir(path):
    if os.path.splitext(filename)[1] == ".jpg" or os.path.splitext(filename)[1] == ".png" or os.path.splitext(filename)[1] == ".JPEG":
        try:
            img = Image.open(os.path.join(path, filename))
            # print(filename.replace(".jpeg", ".jpg"))
            # newfilename = "0000" + str(i) + ".jpg"
            # not rename first
            newfilename = os.path.splitext(filename)[0] + '.jpg'
            img.save(os.path.join(new_path, newfilename))
            i = i + 1
            print(i)
        # 如果读取文件错误啥的就把这个文件删了吧
        except:
            print("{} is broken, deleted!".format(filename))
            os.remove(os.path.join(path, filename))
print("Totally transfer %d images" % i)
