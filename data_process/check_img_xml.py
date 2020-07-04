# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-13
'''
import os

xml_path = "/jimmy/darknet/scripts_5/axe/Annotations/"
img_path = "/jimmy/darknet/scripts_5/axe/JPEGImages/"

for xml_file in os.listdir(xml_path):
    xml_name = os.path.splitext(xml_file)[0]
    flag = False
    for img_file in os.listdir(img_path):
        img_name = os.path.splitext(img_file)[0]
        if xml_name == img_name:
            flag = True
            break
    if flag == False:
        print(xml_name)
        # os.remove(os.path.join(xml_path, xml_file))
        print("Deleted " + xml_file )
    flag = False

# 换一下继续遍历
temp = xml_path
xml_path = img_path
img_path = temp

for xml_file in os.listdir(xml_path):
    xml_name = os.path.splitext(xml_file)[0]
    flag = False
    for img_file in os.listdir(img_path):
        img_name = os.path.splitext(img_file)[0]
        if xml_name == img_name:
            flag = True
            break
    if flag == False:
        print(xml_name)
        # os.remove(os.path.join(xml_path, xml_file))
        print("Deleted " + xml_file)
    flag = False
    