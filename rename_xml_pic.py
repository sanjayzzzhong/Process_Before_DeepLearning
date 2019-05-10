#coding:utf-8
from PIL import Image
import os.path
import glob
import xml.etree.ElementTree as ET
import xml.dom.minidom
 
i = 5979
xmldir = "/home/sanjay/DATA/Project_Datasets/manhole1/xml/"
imgsdir = "/home/sanjay/DATA/Project_Datasets/manhole1/img/"
#outdir = "/home/sanjay/Pictures/manhole_1/new"
for xmlfile in os.listdir(xmldir):
    xmlname = os.path.splitext(xmlfile)[0]
    # print(os.path.splitext(xmlfile))
    for pngfile in os.listdir(imgsdir):
        pngname = os.path.splitext(pngfile)[0]
        #print(os.path.splitext(pngfile))
        if pngname == xmlname:
             # 修改图片文件名
             # 图片文件名修改前后的路径
             olddir = os.path.join(os.path.abspath(imgsdir), pngname + ".jpg")
             #print(olddir)
             newdir = os.path.join(os.path.abspath(imgsdir), str(i)+".jpg")
             os.rename(olddir, newdir)
             print(xmlfile, '----->', str(i) + '.jpg')
             # 修改filename结点属性
             # 读取xml文件
             dom = xml.dom.minidom.parse(os.path.join(xmldir, xmlfile))
             root = dom.documentElement
 
             # 获取标签对filename之间的值并赋予新值i
             root.getElementsByTagName('filename')[0].firstChild.data = str(i) + '.jpg'
 
             # 将修改后的xml文件保存
             # xml文件修改前后的路径
             old_xmldir = os.path.join(xmldir, xmlfile)
             new_xmldir = os.path.join(xmldir, str(i)+'.xml')
             # 打开并写入
             with open(old_xmldir, 'w') as fh:
                 dom.writexml(fh)
             os.rename(old_xmldir, new_xmldir)
             i += 1
print('total number is ', i)