# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-13
'''
#coding:utf-8
from PIL import Image
import os.path
import glob
import xml.etree.ElementTree as ET
import xml.dom.minidom
from shutil import copyfile
 
i = 779
xmldir = "/home/sanjay/DATA/Project_Datasets/1_City_Project/已标注数据/2_8月15日/2_原图和标注/第二次数据标注（含原图）/第二次数据标注/井盖/标注后/"
new_xml_dir = "/home/sanjay/DATA/Project_Datasets/1_City_Project/已标注数据/2_8月15日/2_原图和标注/第二次数据标注（含原图）/第二次数据标注/井盖/label/"
imgdir = "/home/sanjay/DATA/Project_Datasets/1_City_Project/已标注数据/2_8月15日/2_原图和标注/第二次数据标注（含原图）/第二次数据标注/井盖/原图/"
#outdir = "/home/sanjay/Pictures/manhole_1/new"
for xmlfile in os.listdir(xmldir):
    # get xml filename without suffix
    xmlname = os.path.splitext(xmlfile)[0]
    # get xml file dom
    dom = xml.dom.minidom.parse(os.path.join(xmldir, xmlfile))
    root = dom.documentElement

    # 获取标签对filename之间的值并赋予新值i
    real_name = str(root.getElementsByTagName('filename')[0].firstChild.data)
    real_file_name = real_name[:-4]
    print(real_file_name)
    for imgfile in os.listdir(imgdir):
        imgname = os.path.splitext(imgfile)
        print(imgname[0] == real_file_name)
        if(imgname[0] == real_file_name):
            old_xmldir = os.path.join(xmldir, xmlfile)
            new_xmldir = os.path.join(new_xml_dir, real_file_name + ".xml")
            #rename
            copyfile(old_xmldir, new_xmldir)