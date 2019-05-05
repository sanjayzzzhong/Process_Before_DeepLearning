
#%%
import numpy as np
import os
import sys
import tensorflow as tf
import cv2
import time
 
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
 
start = time.time()
#TF_CPP_MIN_LOG_LEVEL默认值为 0 (显示所有logs)，设置为 1 隐藏 INFO logs, 2 额外隐藏WARNING logs, 设置为3所有 ERROR logs也不显示。
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
cv2.setUseOptimized(True)  # 加速cv
 
# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
 
# 可能要改的内容
######################################################
PATH_TO_CKPT = 'rfcn_inference_graph_v1/frozen_inference_graph.pb'  # 模型及标签地址
 
PATH_TO_LABELS = 'data/manhole.pbtxt'
 
video_PATH = "manhole_original/net_test.mp4"  # 要检测的视频
out_PATH = "net_demo_v2.mp4"  # 输出地址
 
NUM_CLASSES = 3  # 检测对象个数
 
fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # 编码器类型（可选）
# 编码器： DIVX , XVID , MJPG , X264 , WMV1 , WMV2


#%%
# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# 加载 标签map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)

category_index = label_map_util.create_category_index(categories)


#%%
# 读取视频
video_cap = cv2.VideoCapture(video_PATH)
fps = int(video_cap.get(cv2.CAP_PROP_FPS))  # 帧率

# 视频的宽和高
width = int(video_cap.get(3))  
hight = int(video_cap.get(4))
 
videoWriter = cv2.VideoWriter(out_PATH, fourcc, fps, (width, hight))


config = tf.ConfigProto()
# 减小显存占用
config.gpu_options.allow_growth = True 


#%%
with detection_graph.as_default():
    with tf.Session(graph=detection_graph, config=config) as sess:
        num = 0
        while True:
            ret, frame = video_cap.read()
            # ret返回False表示没有读到帧，这是视频结束的跳出逻辑
            if ret == False:
                break
            num += 1
            
            print(num)
            # print(num/fps) # 检测到第几秒了

            image_np = frame
            # 增加第一个维度，
            image_np_expanded = np.expand_dims(image_np, axis=0)
            #############下面都是通过tensorname获取值############################
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            #####################################################################

            # Actual detection.
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})

            # 可视化，squeeze是将维度为1的压缩没了，如(1,2,3)经过squeeze变成了(2,3)
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=4)

            # 写视频
            videoWriter.write(image_np)
# 释放videoWriter对象占用的资源
videoWriter.release()
end = time.time()
print("Execution Time: ", end - start)


#%%



