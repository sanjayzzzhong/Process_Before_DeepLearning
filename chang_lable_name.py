# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-13
'''
# coding=utf-8
import os
import os.path
import xml.dom.minidom

#获得文件夹中所有文件
FindPath = '/home/sanjay/DATA/Project_Datasets/Tibet_Project/Knife/n03973628/Annotation/n03973628/'
FileNames = os.listdir(FindPath)
s = []
# new xml path to save
xml_path = '/home/sanjay/DATA/Project_Datasets/Tibet_Project/Knife/knife_xml/'
# iterate all file just with file_name without path, just filename, such as '0.xml'
for file_name in FileNames:
    if not os.path.isdir(file_name):  # 判断是否是文件夹,不是文件夹才打开
        print(file_name)

    #读取xml文件
    # os.path.join(FindPath, file_name) which is an absolute path
    dom = xml.dom.minidom.parse(os.path.join(FindPath,file_name))

    # 获取xml文件的根节点
    root = dom.documentElement

    # 获取标签对name之间的值
    name = root.getElementsByTagName('name')
    for i in range(len(name)):
        print(name[i].firstChild.data)
        if name[i] .firstChild.data== 'n03973628':
            name[i].firstChild.data = 'knife'
            print('修改后的 name')
            print(name[i].firstChild.data)
        # elif name[i].firstChild.data == '1d':
        #     name[i].firstChild.data = '1'
        #     print('修改后的 name')
        #     print(name[i].firstChild.data)
        # elif name[i].firstChild.data == '2d':
        #     name[i].firstChild.data = '2'
        #     print('修改后的 name')
        #     print(name[i].firstChild.data)
        # elif name[i].firstChild.data == '3d':
        #     name[i].firstChild.data = '3'
        #     print('修改后的 name')
        #     print(name[i].firstChild.data)
        # elif name[i].firstChild.data == '4d':
        #     name[i].firstChild.data = '4'
        #     print('修改后的 name')
        #     print(name[i].firstChild.data)
        # elif name[i].firstChild.data == '5d':
        #     name[i].firstChild.data = '5'
        #     print('修改后的 name')
        #     print(name[i].firstChild.data)
        # elif name[i].firstChild.data == '6d':
        #     name[i].firstChild.data = '6'
        #     print('修改后的 name')
        #     print(name[i].firstChild.data)
        # elif name[i].firstChild.data == '7d':
        #     name[i].firstChild.data = '7'
        #     print('修改后的 name')
        #     print(name[i].firstChild.data)
        # elif name[i].firstChild.data == '8d':
        #     name[i].firstChild.data = '8'
        #     print('修改后的 name')
        #     print(name[i].firstChild.data)
        # elif name[i].firstChild.data == '9d':
        #     name[i].firstChild.data = '9'
        #     print('修改后的 name')
        #     print(name[i].firstChild.data)
        # if name[i].firstChild.data == 'box':
        #     name[i].firstChild.data = 'box_d'
        #     print('修改后的 name')
        #     print(name[i].firstChild.data)
    #将修改后的xml文件保存
    with open(os.path.join(xml_path, file_name), 'w') as fh:
        dom.writexml(fh)
        print('写入name/pose OK!')