import os
import cv2
import sys
from PIL import Image

path = "/home/sanjay/Pictures/dataset/manhole_step2/img"
new_path = "/home/sanjay/Pictures/dataset/manhole_step2/img_new"
i = 1
for filename in os.listdir(path):
    if os.path.splitext(filename)[1] == ".JPEG":
        img = Image.open(os.path.join(path, filename))
        # print(filename.replace(".jpeg", ".jpg"))
        # newfilename = "0000" + str(i) + ".jpg"
        # not rename first
        newfilename = os.path.splitext(filename)[0] + '.jpg'
        img.save(os.path.join(new_path, newfilename))
        i = i + 1
        print(i)
print("Totally transfer %d images" % i)
