import PIL.Image as Image
# import pylab
import imageio
# 注释的代码执行一次就好，以后都会默认下载完成
# imageio.plugins.ffmpeg.download()  #第一次运行是删除注释，下载ffmpeg工具
import skimage
# import numpy as np
import os
from subprocess import call
from tqdm import tqdm
import shutil,os

# 视频的绝对路径和图片存储的目标路径


def extract_frames(src_path, target_path):

    new_path = target_path
    print(new_path)

    for video_name in tqdm(os.listdir(src_path)):
        #video_name = "ZJL35.mp4"
        filename = src_path + video_name
        print(filename)
        cur_new_path = new_path+video_name.split('.')[0]+'/'
        if not os.path.exists(cur_new_path):
            os.mkdir(cur_new_path)
        dest = cur_new_path + video_name.split('.')[0]+'-%04d.jpg'
        print("spliting...\n")
        call(["ffmpeg", "-i", filename, "-r", "5", dest])  # 这里的5为5fps，帧率可修改
        # call(["ffmpeg", "-i", filename, "-r", "5", "-vf", "fps=fps=1/60", "-qscale:v", "2", dest])

def move_all_files_to_another_folder(src_folder, dest_folder):
  new_path=dest_folder
  for derName, subfolders, filenames in os.walk(src_folder):
      print(derName)
      print(subfolders)
      print(filenames)
      for i in range(len(filenames)):
          if filenames[i].endswith('.jpg'):
              file_path=derName+'/'+filenames[i]
              newpath=new_path+'/'+filenames[i]
              shutil.copy(file_path,newpath)

if __name__ == "__main__":
  src_path = "/Users/sanjay/Downloads/test_data/neg/"
  target_path = "/Users/sanjay/Downloads/test_data/frame1/"
  final_path = "/Users/sanjay/Downloads/test_data/all"
  # extract_frames(src_path, target_path)
  move_all_files_to_another_folder(target_path, final_path)
