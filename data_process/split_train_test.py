# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-10
'''

##深度学习过程中，需要制作训练集和验证集、测试集。

import os, random, shutil
def moveFile(img_dir, xml_dir, new_img_dir, new_xml_dir):
        pathDir = os.listdir(img_dir)    #列出所有图片的原始路径
        filenumber = len(pathDir)
        rate = 0.3    #自定义抽取图片的比例，比方说100张抽10张，那就是0.1
        picknumber = int(filenumber*rate) #按照rate比例从文件夹中取一定数量图片
        sample = random.sample(pathDir, picknumber)  #随机选取picknumber数量的样本图片
        print (sample)
        for filename in sample:
            # os.path.splitext(“文件路径”)    分离文件名与扩展名；默认返回(fname,fextension)元组，可做分片操作
            print(filename)
            name = os.path.splitext(filename)[0]
            xml_name = name + ".xml"
            # 移动图片
            shutil.move(img_dir + filename, new_img_dir + filename)
            # 移动xml文件
            shutil.move(xml_dir + xml_name, new_xml_dir + xml_name)
        return

if __name__ == '__main__':
    img_dir = "/yolov3/data/knife/img/"    #源图片文件夹路径
    xml_dir = "/yolov3/data/knife/xml/"
    new_img_dir = '/yolov3/data/knife/images/val/'    #移动到新的文件夹路径
    new_xml_dir = '/yolov3/data/knife/labels/val/'
    moveFile(img_dir, xml_dir, new_img_dir, new_xml_dir)

