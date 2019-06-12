# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-14
'''
'''
# file_name: image_to_CSV.py
这个脚本要运行两遍，第一遍生成训练的，第二遍生成测试的
只需修改三处，
第一和第二处改成:对应的图片文件夹目录，比如说你要生成训练的csv就写train的目录，测试的就写test的目录:
1.os.chdir('D:\\python3\\models-master\\research\\object_detection\\images\\train')
2.path = 'D:\\python3\\models-master\\research\\object_detection\\images\\train'
第三处改成对应的文件名，这里训练写了train.csv，测试的写了test.csv:
3.xml_df.to_csv('train.csv', index=None)
'''
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

# 这里是要修改的第一处和第二处，两个路径相同
os.chdir('/home/sanjay/DATA/Project_Datasets/Tibet_Project/tibet')
path = '/home/sanjay/DATA/Project_Datasets/Tibet_Project/tibet/test_xml'

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    xml_path = path
    xml_df = xml_to_csv(xml_path)
    # 这里是要修改的第三处，第一次运行写train.csv，第二次修改为test.csv
    xml_df.to_csv('train.csv', index=None)
    print('Successfully converted xml to csv.')

main()