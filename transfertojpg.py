import os
import cv2
import sys
from PIL import Image

path = "/home/sanjay/DATA/Dataset/meter_with_label/mechanical_meter/img/"
new_path = "/home/sanjay/DATA/Dataset/meter_with_label/mechanical_meter/new_img/"
i = 1
for filename in os.listdir(path):
    if os.path.splitext(filename)[1] == ".jpg":
        try:
            img = Image.open(os.path.join(path, filename))
            # print(filename.replace(".jpeg", ".jpg"))
            # newfilename = "0000" + str(i) + ".jpg"
            # not rename first
            newfilename = os.path.splitext(filename)[0] + '.jpg'
            img.save(os.path.join(new_path, newfilename))
            i = i + 1
            print(i)
        # 如果读取文件错误啥的就把这个文件删了吧
        except:
            print("{} is broken, deleted!".format(filename))
            os.remove(os.path.join(path, filename))
print("Totally transfer %d images" % i)
