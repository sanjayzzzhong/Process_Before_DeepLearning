import glob
import cv2
import os

WSI_MASK_PATH = '/home/sanjay/DATA/Dataset/meter_with_label/elec_img'   #存放图片的文件夹路径
paths = glob.glob(os.path.join(WSI_MASK_PATH, '*.jpg'))
paths.sort()

for path in paths:
    img = cv2.imread(path)
    print(img.shape)