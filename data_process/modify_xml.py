#coding:utf-8
from PIL import Image
import os.path
import glob
import xml.etree.ElementTree as ET
import xml.dom.minidom

i=1
xmldir = "/home/sanjay/Pictures/data/xml"
for xmlfile in os.listdir(xmldir):
    xmlname = os.path.splitext(xmlfile)[0]
    # print(os.path.splitext(xmlfile))
        # 读取xml文件
    dom = xml.dom.minidom.parse(os.path.join(xmldir, xmlfile))
    root = dom.documentElement
    # 获取标签对filename之间的值并赋予新值i
    root.getElementsByTagName('folder')[0].firstChild.data = '.JPEG'

    
    root.getElementsByTagName('path')[0].firstChild.data = '.JPEG'
    # 将修改后的xml文件保存
    # xml文件修改前后的路径
    old_xmldir = os.path.join(xmldir, xmlfile)
#new_xmldir = os.path.join(xmldir, str(i)+'.xml')
# 打开并写入
    with open(old_xmldir, 'w') as fh:
        dom.writexml(fh)
        #os.rename(old_xmldir, new_xmldir)
    i += 1
print('total number is ', i)