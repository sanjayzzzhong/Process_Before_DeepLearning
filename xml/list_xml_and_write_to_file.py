# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-11-14 20:06:03
'''
import os
xml_path = "/home/sanjay/DATA/Project_Datasets/2_Tibet_Project/1_Gun/gun_classify/ak/xml"
output_file = "/home/sanjay/Workspace/Process_Before_DeepLearning/xml/train_ak.txt"
list_file = os.listdir(xml_path)

train_file = open(output_file, 'a')

for filename in list_file:
    train_file.write(filename + '\n')

train_file.close()