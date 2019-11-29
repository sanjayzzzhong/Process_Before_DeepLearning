# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-11-17 16:43:47
'''
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
# from scipy.msic import imread
from imageio import imread
 
filepath = '/home/sanjay/DATA/Project_Datasets/2_Tibet_Project/1_Gun/gun_classify/pistol/reshape'  # 数据集目录
pathDir = os.listdir(filepath)
 
R_channel = 0
G_channel = 0
B_channel = 0
for idx in range(len(pathDir)):
    #one_depth = []
    filename = pathDir[idx]
    img = imread(os.path.join(filepath, filename)) / 255.0
    print(img.shape)
    print(filename)
    
    R_channel = R_channel + np.sum(img[:, :, 0])
    G_channel = G_channel + np.sum(img[:, :, 1])
    B_channel = B_channel + np.sum(img[:, :, 2])
 
num = len(pathDir) * 512 * 512  # 这里（512,512）是每幅图片的大小，所有图片尺寸都一样
R_mean = R_channel / num
G_mean = G_channel / num
B_mean = B_channel / num
 
R_channel = 0
G_channel = 0
B_channel = 0
for idx in range(len(pathDir)):
    filename = pathDir[idx]
    img = imread(os.path.join(filepath, filename)) / 255.0
    R_channel = R_channel + np.sum((img[:, :, 0] - R_mean) ** 2)
    G_channel = G_channel + np.sum((img[:, :, 1] - G_mean) ** 2)
    B_channel = B_channel + np.sum((img[:, :, 2] - B_mean) ** 2)
 
R_var = np.sqrt(R_channel / num)
G_var = np.sqrt(G_channel / num)
B_var = np.sqrt(B_channel / num)
print("R_mean is %f, G_mean is %f, B_mean is %f" % (R_mean, G_mean, B_mean))
print("R_var is %f, G_var is %f, B_var is %f" % (R_var, G_var, B_var))