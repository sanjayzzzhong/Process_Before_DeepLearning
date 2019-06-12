# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-23
@Filename: conver_annotation.py
这个文件的作用主要是将xml标记文件转换为YOLOv3的相对标记位置坐标,并生成txt文件记录图片的绝对路径
'''

# 导入解析xml文件的包
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

# 要修改的
sets=[('knife', 'train'), ('knife', 'val')]

# 你的分类
classes=['knife']

# 把标记信息转为yolo的相对框信息
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

# 标记文件信息的转换
def convert_annotation(folder, image_id):
    in_file = open('%s/Annotations/%s.xml'%(folder, image_id))
    out_file = open('%s/labels/%s.txt'%(folder, image_id), 'w')
    #将特定的xml文件的根节点解析为树
    tree=ET.parse(in_file)
    # 获取根节点
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# 获取当前工作目录
wd = getcwd()

for folder, image_set in sets:
    # 如果没有labels这个目录，便创建
    if not os.path.exists('%s/labels/'%(folder)):
        os.makedirs('%s/labels/'%(folder))
    
    # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
    # 注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。
    # str.split(str="", num=string.count(str)).
    # 获取所有图片的名字，返回列表
    image_ids = open('%s/ImageSets/Main/%s.txt'%(folder, image_set)).read().strip().split()
    # 在当前文件夹下生成一个文件，方便以后将其合成为一个
    list_file = open('%s_%s.txt'%(folder, image_set), 'w')
    for image_id in image_ids:
        # 将图片的绝对路径写入list_file中
        list_file.write('%s/%s/JPEGImages/%s.jpg\n'%(wd, folder, image_id))
        # 将对应imag_id的xml文件写到labels中的.txt文件中
        convert_annotation(folder, image_id)
    list_file.close()

#os.system("cat danger_train.txt danger_val.txt  > train.txt")