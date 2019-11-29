''' 
tool to build dataset 'pedestrian' it take video and annotate all frames
input: path to video directory
output: annotated frames for each video + videos

to run
CUDA_VISIBLE_DEVICES=0 python Anotate_from_video.py /media/saghir/MEDIA/OSPD/LiveRecord/*.dav
'''


import os, sys
import cv2
import time
#from skvideo.io import VideoCapture
import argparse
import multiprocessing
import numpy as np
import tensorflow as tf
import matplotlib.patches as patches
from lxml import etree
import pathlib

from utils import FPS, WebcamVideoStream
from multiprocessing import Queue, Pool
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

CWD_PATH = os.getcwd()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = os.path.join('/media/saghir/MyHome/models/faster_detector/frozen_inference_graph00003.pb')
#PATH_TO_CKPT = os.path.join('/home/saghir/person_detection/models/model/faster_rcnn_inception_resnet_v2_inference_00003', 'frozen_inference_graph.pb')

PATH_TO_LABELS = './object-detection.pbtxt'

NUM_CLASSES = 1
min_score_thresh=0.40

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)
OUTPUT_PATH = '/media/saghir/MEDIA/OSPD/output_dataset'

def detect_objects(video_name, k,image_np, sess, detection_graph):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    #print("starting detection ...............")
    # Actual detection.
    t = time.time()
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    #print('_______-------------elapsed time: {:.2f}'.format(time.time() - t))
    #print("number of detection %d "% num_detections)
    boxes=np.squeeze(boxes)
    classes=np.squeeze(classes).astype(np.int32)
    scores=np.squeeze(scores)

    n=0
    for i in range(100):
       if classes[i]==1 and scores[i] >= min_score_thresh:
          n=n+1
    print('Detections:   %d '% (n))
    #print(classes)
    classs=np.zeros((n))
    scorss=np.zeros((n))
    boxx=np.zeros((n,4))
    height, width = image_np.shape[:2] 
    j=0
    #fig,ax = plt.subplots(1)
    #ax.imshow(image_np)
    for i in range(100):
       if classes[i]==1 and scores[i] >= min_score_thresh:
           classs[j]=classes[i]
           scorss[j]=scores[i]
           y1,x1,y2,x2=boxes[i]
           boxx[j]=y1*height,x1*width,y2*height-y1*height,x2*width-x1*width
           j=j+1
           rect = patches.Rectangle((x1*width,y1*height),x2*width-x1*width,y2*height-y1*height,linewidth=2,edgecolor='red',facecolor='none')
           #ax.add_patch(rect)
    #plt.show()

    # 为识别出来的帧创建xml文件
    #create xml file for the frame
    root = etree.Element("annotation")
    etree.SubElement(root,"filename").text= video_name + '_{}.jpg'.format(int(k))
    for i in range(n):
      obj=etree.SubElement(root,"object")
      etree.SubElement(obj,"name").text='Person'
      etree.SubElement(obj,"pose").text='Unspecified'
      etree.SubElement(obj,"difficult").text='0'
      occlusion=etree.SubElement(obj,"occlusion")
      etree.SubElement(occlusion,"ratio").text='0'
      etree.SubElement(occlusion,"part").text='None'
      bndbox=etree.SubElement(obj,"bndbox")
      etree.SubElement(bndbox,"xmin").text='{}'.format(int(boxx[i,1]))
      etree.SubElement(bndbox,"ymin").text='{}'.format(int(boxx[i,0]))
      etree.SubElement(bndbox,"width").text='{}'.format(int(boxx[i,3]))
      etree.SubElement(bndbox,"height").text='{}'.format(int(boxx[i,2]))
    tree = etree.ElementTree(root)
    tree.write(OUTPUT_PATH + '/Frames/' + video_name + '/' +video_name + '_{}.xml'.format(int(k)), pretty_print=True, xml_declaration=True)
    cv2.imwrite(OUTPUT_PATH + '/Frames/' + video_name + '/' +video_name + '_{}.jpg'.format(int(k)),image_np)
    #print("successfully created frame and it's corresponding annotation file xml")


    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        boxes,
        classes,
        scores,
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=None,
        min_score_thresh=min_score_thresh,
        line_thickness=2)
    return image_np

if __name__ == '__main__':
    # Load a (frozen) Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        session_config = tf.ConfigProto(allow_soft_placement=True,log_device_placement=False)
        session_config.gpu_options.allow_growth=True
        sess = tf.Session(graph=detection_graph, config = session_config)
    #create directory for output videos and Images
    pathlib.Path(OUTPUT_PATH + '/Videos').mkdir(parents=True, exist_ok=True) 
    pathlib.Path(OUTPUT_PATH + '/Frames').mkdir(parents=True, exist_ok=True) 
    #for each input video
    n=0
    for invideo in sys.argv[1:]:
      n=n+1
      video_capture = cv2.VideoCapture(invideo)
      #extract name and extecsion of each video
      video_name = os.path.splitext(os.path.basename(invideo))[0]
      extension = os.path.splitext(os.path.basename(invideo))[1]
      pathlib.Path(OUTPUT_PATH + '/Frames/' + video_name).mkdir(parents=True, exist_ok=True) 

      fourcc = cv2.VideoWriter_fourcc(*'XVID')
      #out = cv2.VideoWriter(OUTPUT_PATH + '/Videos/' + video_name + "_output" + extension,fourcc, 25.0, (1280,720))
      out = cv2.VideoWriter(OUTPUT_PATH + '/Videos/' + video_name + "_output.mp4",fourcc, 24.0, (1920,1080))
      i=0
      while True:
        ret, frame = video_capture.read()
        if ret==False:
            break
        print(n+1, i, ret)
        if i>0:  #start from frame No. 10
          if ret==True:
             t = time.time()
             out_frame = detect_objects(video_name, i, frame, sess, detection_graph)
             print('videElapsed time: {:.2f}'.format(time.time() - t))
             #cv2.putText(out_frame,'Frame: %d'%(i), (20,50), cv2.FONT_HERSHEY_TRIPLEX, 2, 3000)
             font                   = cv2.FONT_HERSHEY_SIMPLEX
             bottomLeftCornerOfText = (10,500)
             fontScale              = 1
             fontColor              = (255,255,255)
             lineType               = 2

             cv2.putText(out_frame,'Frame: %d'%(i), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
             i=i+1
             out.write(out_frame)
        else:
             i=i+1
      video_capture.release()
      out.release()
      #cv2.destroyAllWindows()
    sess.close()

