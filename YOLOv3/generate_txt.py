# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-23
'''
import os
from os import listdir, getcwd
from os.path import join
if __name__ == '__main__':
    # 图片路径
    source_folder='/yolov3/data/knife/JPEGImages/'
    # 产生train.txt的路径
    dest='/yolov3/data/knife/ImageSets/Main/train.txt' 
    # 生成val.txt的路径
    dest2='/yolov3/data/knife/ImageSets/Main/val.txt'
    # 列出所有图片
    file_list=os.listdir(source_folder)
    # 打开train.txt,以附加的形式打开
    train_file=open(dest,'a')
    val_file=open(dest2,'a')

    # 看看文件一共有多少
    num_images = len(file_list)
    # 自定义训练集和测试的比例
    rate = 0.7 #就是10张图片7张训练，3张验证

    num_train = int(num_images * rate)
    print("The number of train is {}".format(num_train))
    print("The number of validation is {}".format(num_images-num_train))

    for i, file_obj in enumerate(file_list):
        file_path=os.path.join(source_folder,file_obj)
        file_name,file_extend=os.path.splitext(file_obj)

        i += 1
        # 如果还在num_train的范围内，就把文件名字写到train_file中
        if(i <= num_train):
            train_file.write(file_name+'\n')
        # 否者就写刀val_file中
        else :
            val_file.write(file_name+'\n')
    # 关闭文件流，释放资源
    train_file.close()
    val_file.close()
