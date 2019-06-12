# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-05-12
'''

# 导入代码库
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
import cv2

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


##################################定义鼠标的回调函数##########################
start, end = (0, 0), (0, 0)
drawing = False
# roi = np.zeros((500, 500,3), dtype=np.uint8)
last_start, last_end = (0, 0), (0, 0)

# 定义回调函数
def mouse_event(event, x, y, flags, param):
    global start, end, drawing, tmp, roi # 为什么tmp也要使用全局呢，因为tmp是copy来的，要在tmp上获取x，y并且画图
    
    # 鼠标按下，开始画图：记录下起点
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start = (x, y)
    # 实时移动的位置作为矩形的终点
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end = (x, y)
    # 鼠标停止后，停止绘图
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False 
        cv2.rectangle(img, start, (x, y), (0, 0, 255), 10) 
        # 要加下面这句
        # roi = tmp[start[1]:y, start[0]:x]
        last_end = (x, y)

        start = end = (0,0)

###############################################################################



# 加载封装好的模型
MODEL_NAME = 'meter_inference_graph'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='') 


#加载标签映射文件，label_map中文叫做标签映射
NUM_CLASSES = 3
PATH_TO_LABELS = 'data/manhole.pbtxt'
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# 图片数据转换为numpy的ndarray对象
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


# 从文件夹中随机选10张图片
import random
dir_path = 'test_images'
imageName_list = os.listdir(dir_path)
imagePath_list = [os.path.join(dir_path, imageName) for imageName in imageName_list]
# 如果不用随机，将下面语句改为
# selected_imagePath_list = imagePath_list
selected_imagePath_list = random.sample(imagePath_list, 10)



# 用10张图片测试模型的目标检测效果
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        # Definite input and output Tensors for detection_graph
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        for i, imagePath in enumerate(selected_imagePath_list):
            # 读入图片
            img = cv2.imread(imagePath)
            cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
            cv2.setMouseCallback('image', mouse_event)
            while(True):
                tmp = np.copy(img)
                if(drawing and end != (0,0)):
                    cv2.rectangle(tmp, start, end, (0, 0, 255), 10)
                cv2.imshow('image', tmp)
                # 这个时候
            image = Image.open(imagePath)
            # the array based representation of the image will be used later in order to prepare the
            # result image with boxes and labels on it.
            try:
                image_np = load_image_into_numpy_array(image)
            except:
                continue
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            (boxes, scores, classes, num) = sess.run(
              [detection_boxes, detection_scores, detection_classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
              image_np,
              np.squeeze(boxes),
              np.squeeze(classes).astype(np.int32),
              np.squeeze(scores),
              category_index,
              use_normalized_coordinates=True,
              line_thickness=8)
            #plt.figure(figsize=(12,24))
            #plt.imshow(image_np)
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            cv2.imwrite("{}.jpg".format(i), image_bgr)

#plt.show()




