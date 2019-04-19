import glob
import cv2
import os

WSI_MASK_PATH = '/home/sanjay/Downloads/manhole_label/image'   #存放图片的文件夹路径
paths = glob.glob(os.path.join(WSI_MASK_PATH, '*.jpg'))
paths.sort()

for path in paths:
    img = cv2.imread(path)
    print(img.shape)