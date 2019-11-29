# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-13
'''
import os

reflection_path = "/home/sanjay/FDisk/Reflection_Projects/perceptual-reflection-removal/synthetic/transmission_layer/"
transimission_path = "/home/sanjay/FDisk/Reflection_Projects/perceptual-reflection-removal/synthetic/reflection_layer/"

for re_file in os.listdir(reflection_path):
    re_name = os.path.splitext(re_file)[0]
    flag = False
    for tr_file in os.listdir(transimission_path):
        tr_name = os.path.splitext(tr_file)[0]
        if re_name == tr_name:
            flag = True
            break
    if flag == False:
        print(re_name)
        os.remove(os.path.join(reflection_path, re_file))
        print("Deleted " + re_file)
    flag = False
    