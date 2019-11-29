# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-04-19 16:40:25
'''
from PIL import Image     
import os       
path = '/home/sanjay/DATA/Project_Datasets/2_Tibet_Project/1_Gun/gun_classify/pistol/img/' #图片目录 
for file in os.listdir(path):      
     extension = file.split('.')[-1]
     if extension == 'jpg' or extension == 'png':
           fileLoc = path+file
           img = Image.open(fileLoc)
           if img.mode != 'RGB':
                 os.remove(fileLoc)
                 print(file+', '+img.mode)