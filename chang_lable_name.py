# coding=utf-8
import os
import os.path
import xml.dom.minidom

#获得文件夹中所有文件
FindPath = '/home/sanjay/Documents/Tencent Files/1009610720/FileRecv/muck/xml/'
FileNames = os.listdir(FindPath)
s = []
xml_path = '/home/sanjay/Documents/Tencent Files/1009610720/FileRecv/muck/new_xml/'
for file_name in FileNames:
    if not os.path.isdir(file_name):  # 判断是否是文件夹,不是文件夹才打开
        print(file_name)

    #读取xml文件
    dom = xml.dom.minidom.parse(os.path.join(FindPath,file_name))

    root = dom.documentElement

    # 获取标签对name之间的值
    name = root.getElementsByTagName('name')
    for i in range(len(name)):
        print(name[i].firstChild.data)
        if name[i] .firstChild.data== 'musk':
            name[i].firstChild.data = 'muck'
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