# -*- coding: utf-8 -*-
#!/usr/bin/env python
import numpy as np
import time
import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("libs/")
import PyFire
import caffe
from optparse import OptionParser
import requests
import time
from datetime import datetime
from flask import Flask , Response ,request
import thread
import random
import string
import json
from flask_restful import Resource, reqparse
import urllib2
import cv2
from flask_sqlalchemy import SQLAlchemy as sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import orm
from struct import pack,unpack
import ffmpy

app = Flask(__name__)

#引入机器学习模型
ptxt="model/deploy.prototxt"
modelname="model/ffww_iter_55000.caffemodel"
meanfile="model/mean.binaryproto"
wordtext="model/ffww_words.txt"

#定义数据库连接并初始化任务相关变量
engine = create_engine('mysql+pymysql://root:root@1.1.1.1/task?charset=utf8', echo=True)
DB_Session = orm.sessionmaker(bind=engine)
conn = DB_Session()
tasks = {}
ids = {}
taskflags={}

# ??住~V??彀~A佛~^课C??住??N彖~G件?J? ??住??住?
pItems=conn.execute("select param_val from r_param where param_name = 'statusRecallUrl'").fetchall()
statusRecallUrl = pItems[0].param_val
pItems=conn.execute("select param_val from r_param where param_name = 'uploadUrl'").fetchall()
uploadUrl = pItems[0].param_val
pItems=conn.execute("select param_val from r_param where param_name = 'nginxUrl'").fetchall()
nginxUrl = pItems[0].param_val



for i in range(0,10):
    tasks["task_"+str(i)] = True

class struct:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

#该函数测试是否可以连通该服务端
@app.route('/')
def home():
    return "welcome use abstract!"

#以下两个函数为增加或减少任务最大个数
@app.route('/addTaskNum',methods=['POST'])
def addTaskNum():
     count =  request.form['count']
     for i in range(len(tasks),len(tasks)+count):
         tasks["task_"+str(i)] = True

@app.route('/delTaskNum',methods=['POST'])
def deleteTaskNum():
     count =  request.form['count']
     for i in range(0,count):
         del tasks["task_"+str(len(tasks)-1)]

#添加任务
@app.route('/addTask',methods=['POST'])
def addTask():
     #接收调度服务器端传过来的参数，并开始任务
     args = reqparse.RequestParser() \
        .add_argument("taskid", type=str, location='json', required=True) \
        .add_argument("functionid", type=str, location='json', required=True) \
        .parse_args()
     print '--------------------------------------------------', args
     for key in tasks:
         if tasks[key]:
              tasks[key] = False
              print key
              taskid = args['taskid']
              ids[taskid] = key
              thread.start_new_thread( exedetect, (key,args['taskid'],args['functionid']) )
              return args['taskid']# id
     return -1

#停止并删除任务
@app.route('/stopTask',methods=['POST'])
def stopTask():
    args = reqparse.RequestParser() \
        .add_argument("taskid", type=str, location='json', required=True) \
        .parse_args()
    id = args['taskid']
    if id != -1:
        taskflags[id] = False
        key = ids[id]
        #print key
        tasks[key] = True
        print(tasks[key])
        del ids[id]
        return key
    else:
        return "no task value"

#该函数为我们处理感兴趣区域字段的方法，仅供参考，roi字段由前端传入，以分号分割，最后返回的为矩形框上角点的x,y坐标已经框的宽度和高度
def getRoi(roi, imgWidth, imgHeight):
    x = 0
    y = 0
    width = 0
    height = 0

    rects = roi.split(';')
    filter(lambda x: len(x) != 0, rects)
    if len(rects) == 4:
        p1 = rects[0]
        p2 = rects[1]
        p3 = rects[2]
        p4 = rects[3]
        xy1 = p1.split(',')
        xy2 = p2.split(',')
        xy3 = p3.split(',')
        xy4 = p4.split(',')
        if len(xy1) == 2 and len(xy2) == 2 and len(xy3) == 2 and len(xy4) == 2:
            x1 = float(xy1[0]) * float(imgWidth)
            y1 = float(xy1[1]) * float(imgHeight)
            x2 = float(xy2[0]) * float(imgWidth)
            y2 = float(xy2[1]) * float(imgHeight)
            x3 = float(xy3[0]) * float(imgWidth)
            y3 = float(xy3[1]) * float(imgHeight)
            x4 = float(xy4[0]) * float(imgWidth)
            y4 = float(xy4[1]) * float(imgHeight)
            minX = min(x1, x2, x3, x4)
            minY = min(y1, y2, y3, y4)
            maxX = max(x1, x2, x3, x4)
            maxY = max(y1, y2, y3, y4)
            width = int(max(maxX - minX, 1))
            height = int(max(maxY - minY, 1))
            x = int(minX)
            y = int(minY)
    return x, y, width, height

#任务具体执行函数
def exedetect(key,islive,taskid,functionid,videourl):
    #初始化任务相关参数
    global taskflags
    global conn
    taskflags[taskid] = True
    name = taskid
    global ptxt
    global modelname
    global meanfile
    global wordtext
    #新建SDK对象
    obj=PyFire.init()
    obj.addNewVideo(name,ptxt,modelname,meanfile,wordtext)
    status = 0

    if islive:
        #即时处理,与离线类似
    else:
        #处理离线视频
        #初始化cv2的视频读取对象，同时定义视频生成的帧率、size、编码等
        i=1
        timeStr = str(time.time())
        cap = cv2.VideoCapture(videourl)
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        size = (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
        print(size)
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        fourcc = int(fourcc)
        bs = pack('i', fourcc)
        fourcc, = unpack('i',bs)
        outVideo = cv2.VideoWriter("/fileDir/"+timeStr+'result.avi',fourcc,fps,size)
        frameNum = 0
        cap = cv2.VideoCapture(videourl)
        #循环读取视频流直到无输入或者被停止
        while True:
            #ret为是否读取到视频帧，frame为该帧
            ret,frame = cap.read()
            if ret == False:
                print "No video input."
                #当没有视频输入了，回调告知前端服务器任务已经结束，并将生成的视频发送到调度服务器的nginx代理，再将该地址回调告知前端服务器
                utilApi.statusRecall(taskid,1,key)
                if frameNum>0:
                    ff = ffmpy.FFmpeg(
                            inputs={"/fileDir/"+timeStr+'result.avi':None},
                            outputs={"/fileDir/"+timeStr+'result.mp4':None}
                    )
                    ff.run()
                    video_name = timeStr+'result.mp4'
                    video_url = "/fileDir/" + video_name
                    files = {'upload_file': (video_name, open(video_url, 'rb'))}
                    url = uploadUrl
                    req =  utilApi.upload(url,files)
                    print req.json()
                    url = notify_url
                    data = {"device_id":device_id,"taskid":taskid,"status":1,"result_video_url":nginxUrl+video_name,"event_date":datetime.now().strftime('%Y-%m-%d'),"event_time":datetime.now().strftime('%H:%M:%S'),"functionid":functionid,"result_desc":"result_desc"}
                    req =  utilApi.recall(url,data)
                    print req.json()
                break
            #当视频已经被停止，则跳出循环
            if taskflags[taskid]==False:
                print "Task is stopped."
                break
            #调用SDK对象检测状态
            obj.Update(name,frame,1)
            nowStatus = obj.getCurrType(name)
            #判断检测到的状态，并用cv2的函数添加文字或者画框
            #画框示例函数为：cv2.rectangle(frame,(int(lx),int(lr)),(int(lx+w),int(lr+h)),(255,0,0),2)，也可以上网自行搜索，有更详细的使用方法
            if status == 0 and nowStatus == 2:
                print "Fire!"
                cv2.putText(frame,'Fire',(5,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
            elif status == 2 and nowStatus == 0:
                status = 0
                cv2.putText(frame,'No fire',(5,30),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1)
            else:
                cv2.putText(frame,'No fire',(5,30),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1)
            frameNum = frameNum+1
            #将当前帧写入视频，如要视频切割可以添加条件，不一定每一帧都写入视频，另外需要保存为图片文件也是对frame对象进行处理
            outVideo.write(frame)
        #释放视频流，并从调度服务器上清除任务，但前端服务器上有保存该任务信息
        cap.release()
        outVideo.release()
        del taskflags[taskid]
        conn.execute("delete from task where taskid ='" + taskid+"'")
        conn.commit()
        conn.close()

#自定义的工具类
class utilApi():
    #回调前端服务器
    @staticmethod
    def recall(url,postdata):
        print postdata
        req = requests.post(url,data=json.dumps(postdata),headers={'Content-Type':'application/json;charset=utf8'})
        print req
        return req
    #上传文件到调度服务器
    @staticmethod
    def upload(url,files):
        data = None
        req = requests.post(url,files=files,data=data)
        print req
        return req
    #将当前状态告知前端服务器
    @staticmethod
    def statusRecall(taskid,status,key):
        global taskflags
        global ids
        url = statusRecallUrl
        taskflags[taskid] = False
        key = ids[taskid]
        #print key
        tasks[key] = True
        print(tasks[key])
        del ids[taskid]
        url = statusRecallUrl
        data = {"taskid":taskid,"status":status,"event_date":datetime.now().strftime('%Y-%m-%d'),"event_time":datetime.now().strftime('%H:%M:%S')}
        req = requests.post(url,data=json.dumps(data),headers={'Content-Type':'application/json;charset=utf8'})
        print req.json()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
