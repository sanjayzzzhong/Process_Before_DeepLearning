# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-13
'''
import os

original_path = "/home/sanjay/Videos/muck_original/"
test_path = "/home/sanjay/Videos/渣土测试图片/muck_test/good/"

for test_file in os.listdir(test_path):
    test_name = os.path.splitext(test_file)[0]
    flag = False
    for original_file in os.listdir(original_path):
        original_name = os.path.splitext(original_file)[0]
        if test_name == original_name:
            flag = True
            break
    if flag == False:
        print(original_name)
        os.remove(os.path.join(original_path, original_file))
        print("Deleted " + original_file)
    flag = False
    