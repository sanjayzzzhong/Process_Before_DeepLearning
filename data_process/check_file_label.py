# coding=utf-8
import os
import os.path
import xml.dom.minidom

#获得文件夹中所有文件
FindPath = '/home/sanjay/DATA/Project_Datasets/Meter_project/digital_meter/label/xml/'
FileNames = os.listdir(FindPath)
s = []
count = 0
# iterate all file just with file_name without path, just filename, such as '0.xml'
for file_name in FileNames:
    if not os.path.isdir(file_name):  # 判断是否是文件夹,不是文件夹才打开
        #print(file_name)
        pass

    #读取xml文件
    # os.path.join(FindPath, file_name) which is an absolute path
    dom = xml.dom.minidom.parse(os.path.join(FindPath,file_name))

    # 获取xml的根节点
    root = dom.documentElement

    # 获取标签对name之间的值
    name = root.getElementsByTagName('name')
    flag = False
    for i in range(len(name)):
        # print(name[i].firstChild.data)
        if name[i] .firstChild.data== '.':
            flag = True
    if flag == False:
        count += 1
        s.append(file_name)

print("There are {} files".format(count))
for file_name in s:
    print(file_name)