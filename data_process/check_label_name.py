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
FindPath = '/home/sanjay/DATA/Project_Datasets/Tibet_Project/Knife/knife/xml'
FileNames = os.listdir(FindPath)

# iterate all file just with file_name without path, just filename, such as '0.xml'
for file_name in FileNames:
    if not os.path.isdir(file_name):  # 判断是否是文件夹,不是文件夹才打开
        #print(file_name)
        pass

    #读取xml文件
    # os.path.join(FindPath, file_name) which is an absolute path
    dom = xml.dom.minidom.parse(os.path.join(FindPath,file_name))

    # 获取xml文件的根节点
    root = dom.documentElement

    # 获取标签对name之间的值
    name = root.getElementsByTagName('name')
    # 标记位
    flag = False
    for i in range(len(name)):
        #print(name[i].firstChild.data)
        if name[i].firstChild.data == 'gun':
            flag = True
        if name[i].firstChild.data == 'knife':
            # flag = True
            pass

    # if flag == False:
    #     print('remove {}'.format(file_name))
    #     os.remove(os.path.join(FindPath, file_name))
    
    # 如果xml文件中有gun的标记，打印这文件的名字
    if flag:
        print(file_name)