##深度学习过程中，需要制作训练集和验证集、测试集。

import os, random, shutil
def moveFile(img_dir, xml_dir, test_dir):
        pathDir = os.listdir(img_dir)    #列出所有图片的原始路径
        filenumber = len(pathDir)
        rate = 0.3    #自定义抽取图片的比例，比方说100张抽10张，那就是0.1
        picknumber = int(filenumber*rate) #按照rate比例从文件夹中取一定数量图片
        sample = random.sample(pathDir, picknumber)  #随机选取picknumber数量的样本图片
        print (sample)
        for filename in sample:
            # os.path.splitext(“文件路径”)    分离文件名与扩展名；默认返回(fname,fextension)元组，可做分片操作
            print(filename)
            name = os.path.splitext(filename)[0]
            xml_name = name + ".xml"
            # 移动图片
            shutil.move(img_dir + filename, test_dir + filename)
            # 移动xml文件
            shutil.move(xml_dir + xml_name, test_dir + xml_name)
        return

if __name__ == '__main__':
    img_dir = "/root/manhole/models/research/object_detection/images/elec_img/"    #源图片文件夹路径
    xml_dir = "/root/manhole/models/research/object_detection/images/elec_xml/"
    test_dir = '/root/manhole/models/research/object_detection/images/meter_test/'    #移动到新的文件夹路径
    moveFile(img_dir, xml_dir, test_dir)















	















	
