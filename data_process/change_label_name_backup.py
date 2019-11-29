# coding=utf-8
import os
import os.path
import xml.dom.minidom

#获得文件夹中所有文件
FindPath = '/home/sanjay/DATA/Dataset/meter_with_label/machinemeter/15.xml/'
FileNames = os.listdir(FindPath)
s = []
xml_path = '/home/sanjay/DATA/Dataset/meter_with_label/machinemeter/15_xml_new/'
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
        if name[i] .firstChild.data== '0_1':
            name[i].firstChild.data = '0'
            print('修改后的 name')
            print(name[i].firstChild.data)
        elif name[i].firstChild.data == '1_2':
            name[i].firstChild.data = '1'
            print('修改后的 name')
            print(name[i].firstChild.data)
        elif name[i].firstChild.data == '2_3':
            name[i].firstChild.data = '2'
            print('修改后的 name')
            print(name[i].firstChild.data)
        elif name[i].firstChild.data == '3_4':
            name[i].firstChild.data = '3'
            print('修改后的 name')
            print(name[i].firstChild.data)
        elif name[i].firstChild.data == '4_5':
            name[i].firstChild.data = '4'
            print('修改后的 name')
            print(name[i].firstChild.data)
        elif name[i].firstChild.data == '5_6':
            name[i].firstChild.data = '5'
            print('修改后的 name')
            print(name[i].firstChild.data)
        elif name[i].firstChild.data == '6_7':
            name[i].firstChild.data = '6'
            print('修改后的 name')
            print(name[i].firstChild.data)
        elif name[i].firstChild.data == '7_8':
            name[i].firstChild.data = '7'
            print('修改后的 name')
            print(name[i].firstChild.data)
        elif name[i].firstChild.data == '8_9':
            name[i].firstChild.data = '8'
            print('修改后的 name')
            print(name[i].firstChild.data)
        elif name[i].firstChild.data == '9_0':
            name[i].firstChild.data = '9'
            print('修改后的 name')
            print(name[i].firstChild.data)
    #将修改后的xml文件保存
    with open(os.path.join(xml_path, file_name), 'w') as fh:
        dom.writexml(fh)
        print('写入name/pose OK!')