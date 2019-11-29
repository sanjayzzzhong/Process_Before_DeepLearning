# coding: utf-8
# 对文件夹里的所有图片进行增强，同时增强bounding box

import imgaug as ia
from imgaug import augmenters as iaa
import os
import xml.etree.ElementTree as ET
import cv2
from PIL import Image
import numpy as np


# 读原始图片xml文件的bounding box坐标，读了这些坐标用于后面得到bounding box对象
def read_annotations(rootDir, img_id):
    file = open(os.path.join(rootDir, img_id))  # open()为内置函数，根据给的路径打开一个文件
    tree = ET.parse(file)  # 解析xml文件 得到树结构
    root = tree.getroot()  # 得到根节点，可以遍历
    bndList = []

    for object in root.findall('object'):  # 遍历根节点下所有的object节点 一张图可能有多个目标
        bndbox = object.find("bndbox")  # 每个目标有个bndbox节点 就是bbs的信息了
        xmin = int(bndbox.find("xmin").text)  # 找xmin节点的text属性 就是具体的值 是字符串，要转成int
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        bndList.append([xmin, ymin, xmax, ymax])  # 一张图片的bbox坐标就存在了一个list里面

    return bndList


def create_annotations(rootDir, img_id, new_target, saveDir, num, removeList):
    file = open(os.path.join(rootDir, img_id+'.xml'))  # 这里每一个逗号就相当于是一个\\，路径之间的那个/,所以后面要用字符串拼接
    tree = ET.parse(file)
    root = tree.getroot()
    index = 0
    objects = root.findall('object')
    removeList.reverse()  # 这里倒置是因为删除多个的话，前面的删除了后面就补上来，再删下一个索引就错了，因为索引都变了，所以要倒着删除 https://blog.csdn.net/u012956540/article/details/50816334
    if len(removeList) != 0:
        for id_remove in removeList:  # 这里用removeList.reverse()的话会报错'NoneType' object is not iterable 因为list.reverse()这个函数没有返回值 也就是返回None
            objects.pop(id_remove)

    # 运行到这里经常报list index out of range这个错，应该是bbox裁剪之后导致原来tree里object的数目和新图片的object数目不一致导致的
    # 本来是想把图片之外的bbox删除的也给删除，但是没有写成功，直接不让图片平移之类的了
    for object in objects:
        bndbox = object.find("bndbox")
        bndbox.find("xmin").text = str(int(new_target[index].x1))  # 一开始是float  当list为空时，取索引0也会报错
        bndbox.find("ymin").text = str(int(new_target[index].y1))
        bndbox.find("xmax").text = str(int(new_target[index].x2))
        bndbox.find("ymax").text = str(int(new_target[index].y2))

        index = index + 1
    tree.write(os.path.join(saveDir, img_id+"_aug_"+str(num)+".xml"))  # 把整个树结构写到新的xml文件里面去
    print("augment success:", img_id+"_aug_"+str(num))


if __name__ == '__main__':  # 啊啊啊啊这里main左右也有两个杠！！
    # 定义增强序列 从官方文档拷过来的示例，说是常用的比较简单的增强序列
    seq = iaa.Sequential([
        iaa.Fliplr(0.5),  # horizontal flips
        iaa.Flipud(0.5),
        iaa.Crop(percent=(0, 0.1)),  # random crops
        # Small gaussian blur with random sigma between 0 and 0.5.
        # But we only blur about 50% of all images.
        iaa.Sometimes(0.5,
                      iaa.GaussianBlur(sigma=(0, 0.5))
                      ),
        # Strengthen or weaken the contrast in each image.
        iaa.ContrastNormalization((0.75, 1.5)),
        # Add gaussian noise.
        # For 50% of all images, we sample the noise once per pixel.
        # For the other 50% of all images, we sample the noise per pixel AND
        # channel. This can change the color (not only brightness) of the
        # pixels.
        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
        # Make some images brighter and some darker.
        # In 20% of all cases, we sample the multiplier once per channel,
        # which can end up changing the color of the images.
        iaa.Multiply((0.8, 1.2), per_channel=0.2),
        # Apply affine transformations to each image.
        # Scale/zoom them, translate/move them, rotate them and shear them.
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            rotate=(-15, 15),
            shear=(-8, 8),
            #mode=ia.ALL,
            #cval=(0, 255)
        )
    ], random_order=True)  # apply augmenters in random order

    IMG_DIR = "C:\\Users\\sunmengtuo\\Desktop\\program\\城市管理项目\\garbage-img\\"
    XML_DIR = "C:\\Users\\sunmengtuo\\Desktop\\program\\城市管理项目\\garbage-annotations\\"
    IMG_AUG_DIR = "C:\\Users\\sunmengtuo\\Desktop\\program\\城市管理项目\\garbage-aug-img\\"
    XML_AUG_DIR = "C:\\Users\\sunmengtuo\\Desktop\\program\\城市管理项目\\garbage-aug-xml\\"
    NUM_LOOP = 4  # 每张图片增强NUM_LOOP次

    imgList = []
    for filename in os.listdir(IMG_DIR):  # os.listdir()列出文件夹下的所有
        if filename.endswith(".jpg"):  # 如果文件是图片
            img = Image.open(os.path.join(IMG_DIR, filename))  # 读图片，是路径，单独这个文件的名字不行，一开始只写了filename报错
            img = np.array(img)
            imgList.append(img)  # 存到List里面
            bndList = read_annotations(XML_DIR, filename[:-4] + ".xml")  # 得到这个图片所有bbox的坐标
            bboxList = []  # 用来放boundingBox对象
            for i in bndList:
                bbox = ia.BoundingBox(i[0], i[1], i[2], i[3])  # 使用坐标去初始化，得到一个BoundingBox对象
                bboxList.append(bbox)  # 把boundingBox对象放在一个list里面
            bbs = ia.BoundingBoxesOnImage(bboxList, shape=img.shape)  # 一张图片上的所有bounding box

            for num in range(NUM_LOOP):  # 每张图片增强NUM_LOOP次
                # Converts this augmenter from a stochastic to a deterministic one.
                # 我理解的意思就是你先用增强器对图片进行增强，然后再用增强器对比如bounding box进行增强，这两次增强如果你不设置这句话，那这两次增强是随机的
                # 设置了这句话两次增强就是一样的效果了 才能保证你增强后的bounding box和增强后的图片是一一对应的 (e.g. if an image is rotated by 30deg, then also rotate its keypoints by 30deg).
                # 就跟随机数设置种子一样
                seq_det = seq.to_deterministic()  # 这个要放在循环里面 因为是每一次才相同，放在外面的话一张图片循环三次，这三次都是一样的变换序列，就得到三张一样的增强图片

                # 变换图像 然后把新图像存起来
                img_aug = seq_det.augment_image(img)

                # 变换bounding box
                bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]  # 返回Augmented bounding boxes  这是对很多图片上的bbox一起进行增强 取0就是取第一张图片上的增强后的bbox，因为我们这里只处理一张
                remove_id_list = []
                for id in range(len(bbs_aug.bounding_boxes)):
                    if bbs_aug.bounding_boxes[id].is_out_of_image(img_aug, fully=True, partly=False):
                        #print(id)
                        remove_id_list.append(id)
                # 变换后有的bbox可能超出图片的范围了 要裁剪一下
                bbs_aug_clip = bbs_aug.remove_out_of_image().clip_out_of_image()
                if bbs_aug_clip:
                    Image.fromarray(img_aug).save(IMG_AUG_DIR + filename[:-4] + "_aug_" + str(num) + ".jpg")
                    # 创建xml文件
                    create_annotations(XML_DIR, filename[:-4], bbs_aug_clip.bounding_boxes, XML_AUG_DIR, num, remove_id_list)
                #else:
                    #Image.fromarray(img_aug).save(IMG_AUG_DIR + filename[:-4] + "_aug_null_" + str(num) + ".jpg")

                # image_after = bbs_aug.draw_on_image(img_aug, thickness=3)
                # image_after_clip = bbs_aug_clip.draw_on_image(img_aug, thickness=3)
                # Image.fromarray(image_after).save(IMG_AUG_DIR+filename[:-4]+"_draw_"+str(num)+".jpg")
                # Image.fromarray(image_after_clip).save(IMG_AUG_DIR + filename[:-4] + "_draw_clip_" + str(num) + ".jpg")
                # for o in range(len(bbs.bounding_boxes)):
                #     print("\nbefore:", bbs.bounding_boxes[o].x1, bbs.bounding_boxes[o].y1, bbs.bounding_boxes[o].x2, bbs.bounding_boxes[o].y2,)
                #     print("\nafter:", bbs_aug.bounding_boxes[o].x1, bbs_aug.bounding_boxes[o].y1, bbs_aug.bounding_boxes[o].x2, bbs_aug.bounding_boxes[o].y2,)


