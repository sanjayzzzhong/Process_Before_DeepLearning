# -*- coding: UTF-8 -*-
'''
@Author: sanjayzhong
@Github: https://github.com/sanjayzzzhong
@Date: 2019-06-11
'''



import numpy as np 
import cv2 

start, end = (0, 0), (0, 0)
drawing = False
roi = np.zeros((500, 500,3), dtype=np.uint8)

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
        roi = tmp[start[1]:y, start[0]:x]
        start = end = (0,0)

img_path = "/home/sanjay/Workspace/Learning_Workspace/IMG_5889.JPG"
img = cv2.imread(img_path)
# 要给窗口命名
cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
#不要忘了设置鼠标的回调函数, 鼠标的回调函数是绑定了名为'image'的窗口上的
cv2.setMouseCallback('image', mouse_event)

cv2.namedWindow('roi', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)

while(True):
    # 拷贝出原图，不改变原图
    tmp = np.copy(img)
    if(drawing and end != (0, 0)):
        cv2.rectangle(tmp, start, end, (0, 0, 255), 10)

    cv2.imshow('image', tmp)
    cv2.imshow('roi', roi)
    if cv2.waitKey(1) == ord('q'):
        break
