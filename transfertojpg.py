import os
import cv2
import sys
from PIL import Image

path = "/home/sanjay/DATA/ChromeDownload/WeaponS/test"
new_path = "/home/sanjay/DATA/ChromeDownload/WeaponS/test_new"
i = 1
for filename in os.listdir(path):
    if os.path.splitext(filename)[1] == ".JPEG" or os.path.splitext(filename)[1] == ".png" or os.path.splitext(filename)[1] == ".jpg" or os.path.splitext(filename)[1] == ".jpeg":
        img = Image.open(os.path.join(path, filename))
        # print(filename.replace(".jpeg", ".jpg"))
        # newfilename = "0000" + str(i) + ".jpg"
        # not rename first
        newfilename = os.path.splitext(filename)[0] + '.jpg'
        img.save(os.path.join(new_path, newfilename))
        i = i + 1
        print(i)
print("Totally transfer %d images" % i)
