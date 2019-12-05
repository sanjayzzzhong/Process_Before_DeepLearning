# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-12-05 12:14:07
'''
'''
输入: 图片目录路径 和 标注文件xml文件夹路径, 以及想要命名的种类
功能:
1. 自动把图片全部都转换为.jpg格式, 如果图片中有深度非3位的 或者 的, 则删除
2. 检查jpg文件和xml文件的对应关系, 如果jpg没有对应的xml文件, 删除jpg; 如果xml没有对应的jpg文件, 删除xml
3. 根据想要命名的种类, 重新命名jpg文件和xml文件, 需要指定i的开始数量
'''

import os
from PIL import Image
import glob
import xml.etree.ElementTree as ET
import xml.dom.minidom

def auto_check_img_xml(img_path, xml_path, new_path, class_name, rename_begin_num):
    # 1. 功能点1
    for i, filename in enumerate(os.listdir(img_path)):
        if os.path.splitext(filename)[1] == ".jpg" or os.path.splitext(filename)[1] == ".png" or os.path.splitext(filename)[1] == ".JPEG" or os.path.splitext(filename)[1] == ".JPG" or os.path.splitext(filename)[1] == ".jpeg":
            try:
                img = Image.open(os.path.join(img_path, filename))
                # 这里不要改名字, 否则和xml文件名对应不起来
                newfilename = os.path.splitext(filename)[0] + '.jpg'
                if os.path.exists(new_path) is False:
                    os.mkdir(new_path)
                img.save(os.path.join(new_path, newfilename))
                print("已保存{}, 第{}张".format(newfilename, i))
            # 如果读取文件错误啥的就把这个文件删了吧
            except Exception as e:
                print("{} is broken, deleted!".format(filename))
                os.remove(os.path.join(img_path, filename)) # not delete yet
    print("Totally transfer %d images" % i)

    # 2. 功能点2
    for xml_file in os.listdir(xml_path):
        xml_name = os.path.splitext(xml_file)[0]
        flag = False
        for img_file in os.listdir(new_path):
            img_name = os.path.splitext(img_file)[0]
            if xml_name == img_name:
                flag = True
                break
        if flag == False:
            os.remove(os.path.join(xml_path, xml_file))
            print("xml没有找到对应的图片, 删除 " + xml_file )
        flag = False

    # 换一下继续遍历
    temp = xml_path
    xml_path = new_path
    new_path = temp

    for xml_file in os.listdir(xml_path):
        xml_name = os.path.splitext(xml_file)[0]
        flag = False
        for img_file in os.listdir(new_path):
            img_name = os.path.splitext(img_file)[0]
            if xml_name == img_name:
                flag = True
                break
        if flag == False:
            os.remove(os.path.join(xml_path, xml_file))
            print("图片找不到对应的xml文件, 删除 " + xml_file)
        flag = False

    
    # 把刚刚的路径换回来
    temp = xml_path
    xml_path = new_path
    new_path = temp
    print(xml_path)
    print(new_path)
    # 3. 功能点3
    for xmlfile in os.listdir(xml_path):
        xmlname = os.path.splitext(xmlfile)[0]
        # print(os.path.splitext(xmlfile))
        for pngfile in os.listdir(new_path):
            pngname = os.path.splitext(pngfile)[0]
            # print(os.path.splitext(pngfile))
            if pngname == xmlname:
                # 修改图片文件名
                # 图片文件名修改前后的路径
                olddir = os.path.join(os.path.abspath(new_path), pngname + ".jpg")
                # print(olddir)
                newdir = os.path.join(os.path.abspath(
                    new_path), class_name + "_" + str(rename_begin_num) + ".jpg")
                os.rename(olddir, newdir)
                print(xmlfile, '----->', str(rename_begin_num) + '.jpg')
                # 修改filename结点属性
                # 读取xml文件
                dom = xml.dom.minidom.parse(os.path.join(xml_path, xmlfile))
                root = dom.documentElement

                # 获取标签对filename之间的值并赋予新值i
                root.getElementsByTagName('filename')[
                    0].firstChild.data = class_name + "_" + str(rename_begin_num) + '.jpg'

                # 将修改后的xml文件保存
                # xml文件修改前后的路径
                old_xmldir = os.path.join(xml_path, xmlfile)
                new_xmldir = os.path.join(xml_path, class_name + "_" + str(rename_begin_num)+'.xml')
                # 打开并写入
                with open(old_xmldir, 'w') as fh:
                    dom.writexml(fh)
                os.rename(old_xmldir, new_xmldir)
                rename_begin_num += 1
    print('total number is ', rename_begin_num)


# 主程序
if  __name__ == "__main__":
    img_path = "/home/sanjay/Documents/Tencent Files/1009610720/FileRecv/ak_pic/ak_2"
    xml_path = "/home/sanjay/Documents/Tencent Files/1009610720/FileRecv/ak_pic/xml2"
    new_path = "/home/sanjay/Documents/Tencent Files/1009610720/FileRecv/ak_pic/new_img2"
    class_name = "ak47"
    begin_num = 3587
    auto_check_img_xml(img_path, xml_path, new_path, class_name, begin_num)