#!/usr/bin/python3
# coding=utf8
import sys
import cv2
import math
import time
import threading
import numpy as np
import apriltag
import RPi.GPIO as GPIO
import HiwonderSDK.Board as Board
import HiwonderSDK.PID as PID
import HiwonderSDK.Misc as Misc
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

AK = ArmIK()
#apriltag检测

# 初始位置
def initMove():
    Board.setBusServoPulse(1, 500, 800)
    Board.setBusServoPulse(2, 500, 800)
    AK.setPitchRangeMoving((0, 10, 18), 0,-90, 0, 1500)

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

def setBuzzer(sleeptime):
    GPIO.setup(6, GPIO.OUT) #设置引脚为输出模式
    GPIO.output(6, 1)       #设置引脚输出高电平
    time.sleep(sleeptime)   #设置延时
    GPIO.output(6, 0)

# 检测apriltag
detector = apriltag.Detector(searchpath=apriltag._get_demo_searchpath())
def apriltagDetect(img):
    global buzzer
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray, return_image=False)

    if len(detections) != 0:
        for detection in detections:                       
            corners = np.rint(detection.corners)  # 获取四个角点
            cv2.drawContours(img, [np.array(corners, np.int)], -1, (0, 255, 255), 2)

            tag_family = str(detection.tag_family, encoding='utf-8')  # 获取tag_family
            tag_id = int(detection.tag_id)  # 获取tag_id

            object_center_x, object_center_y = int(detection.center[0]), int(detection.center[1])  # 中心点
            
            object_angle = int(math.degrees(math.atan2(corners[0][1] - corners[1][1], corners[0][0] - corners[1][0])))  # 计算旋转角
            
            object_area = abs(int((corners[3][1] - corners[0][1]) * (corners[3][0] - corners[0][0])))
            if object_area < 300:
                buzzer = True
            else:
                buzzer = False
            print('Size:',object_area,'Pixel')
            
            return tag_family, tag_id
            
    return None, None


buzzer = False

def move():
    global buzzer
    
    while True:
        if buzzer:
            setBuzzer(0.2)
            time.sleep(0.2)
                
        time.sleep(0.01)
      
# 运行子线程
th = threading.Thread(target=move)
th.setDaemon(True)
th.start()

state = True
def run(img):
    global state
    global buzzer
    global tag_id
    global action_finish
     
    img_h, img_w = img.shape[:2]
    
    tag_family, tag_id = apriltagDetect(img) # apriltag检测
    
    if tag_id is not None:
        if state:
            state = False
        cv2.putText(img, "tag_id: " + str(tag_id), (10, img.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, [0, 255, 255], 2)
        cv2.putText(img, "tag_family: " + tag_family, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, [0, 255, 255], 2)
    else:
        if not state:
            state = True
        buzzer = False
        cv2.putText(img, "tag_id: None", (10, img.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, [0, 255, 255], 2)
        cv2.putText(img, "tag_family: None", (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, [0, 255, 255], 2)
    
    return img

if __name__ == '__main__':
    initMove()
    cap = cv2.VideoCapture(-1) #读取摄像头
    
    while True:
        ret, img = cap.read()
        if ret:
            frame = img.copy()
            Frame = run(frame)           
            cv2.imshow('Frame', Frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            time.sleep(0.01)
    cv2.destroyAllWindows()
