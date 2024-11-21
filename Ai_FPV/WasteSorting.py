#!/usr/bin/python3
# coding=utf8
import sys
import cv2
import math
import time
import threading
import numpy as np
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
import HiwonderSDK.TTS as TTS
import HiwonderSDK.yaml_handle as yaml_handle

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

AK = ArmIK()

# 初始位置
def initMove():
    Board.setBusServoPulse(1, 200, 300)
    Board.setBusServoPulse(2, 500, 500)
    AK.setPitchRangeMoving((0, 10, 10), -90, -30, -90, 1500)

try:
    tts = TTS.TTS()

except:
    print('没有接传感器')

range_rgb = {
    'red':   (0, 0, 255),
    'blue':  (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'gray': (50,50,50),
    'white': (255, 255, 255)}

__target_color = ('red', 'green', 'blue')
detect_color = 'None'
garbage_species = 'None'

lab_data = yaml_handle.get_yaml_data(yaml_handle.lab_file_path)
    
#设置扩展板的RGB灯颜色使其跟要追踪的颜色一致
def set_rgb(color):
    if color == "red":
        Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
        Board.RGB.show()
    elif color == "green":
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 255, 0))
        Board.RGB.show()
    elif color == "blue":
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 255))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 255))
        Board.RGB.show()
    elif color == "gray":
        Board.RGB.setPixelColor(0, Board.PixelColor(50, 50, 50))
        Board.RGB.setPixelColor(1, Board.PixelColor(50, 50, 50))
        Board.RGB.show()
    else:
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
        Board.RGB.show()

# 找出面积最大的轮廓
# 参数为要比较的轮廓的列表
def getAreaMaxContour(contours):
    
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None

    for c in contours:  # 历遍所有轮廓
        contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 300:  # 只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰
                area_max_contour = c

    return area_max_contour, contour_area_max  # 返回最大的轮廓


def move():
    global detect_color
    
    while True:
        if detect_color == 'red':
            tts.TTSModuleSpeak("[h0][v10][m52]", "有害垃圾")
            time.sleep(2)
        elif detect_color == 'green':
            tts.TTSModuleSpeak("[h0][v10][m52]", "厨余垃圾")
            time.sleep(2)      
        elif detect_color == 'blue':
            tts.TTSModuleSpeak("[h0][v10][m52]", "可回收垃圾")
            time.sleep(2)            
        elif detect_color == 'gray':
            tts.TTSModuleSpeak("[h0][v10][m52]", "其他垃圾")
            time.sleep(2)
        detect_color = 'None'
        time.sleep(0.01)
      
# 运行子线程
th = threading.Thread(target=move)
th.setDaemon(True)
th.start()


color_list = []
start_pick_up = False
size = (640, 480)
font_color = (0, 0, 0)
def run(img):
    global rect
    global font_color
    global detect_color
    global start_pick_up
    global color_list
    global garbage_species
        
    img_copy = img.copy()
    frame_resize = cv2.resize(img_copy, size, interpolation=cv2.INTER_NEAREST)
    frame_gb = cv2.GaussianBlur(frame_resize, (3, 3), 3)
    frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间
    color_area_max = None
    max_area = 0
    areaMaxContour_max = 0
    
    if not start_pick_up:
        for i in lab_data:
            if i in __target_color:
                frame_mask = cv2.inRange(frame_lab,
                                             (lab_data[i]['min'][0],
                                              lab_data[i]['min'][1],
                                              lab_data[i]['min'][2]),
                                             (lab_data[i]['max'][0],
                                              lab_data[i]['max'][1],
                                              lab_data[i]['max'][2]))  #对原图像和掩模进行位运算
                opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算
                closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算
                contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓
                areaMaxContour, area_max = getAreaMaxContour(contours)  # 找出最大轮廓
                if areaMaxContour is not None:
                    if area_max > max_area:  # 找最大面积
                        max_area = area_max
                        color_area_max = i
                        areaMaxContour_max = areaMaxContour
        
        if max_area > 500:  # 有找到最大面积
            rect = cv2.minAreaRect(areaMaxContour_max)
            box = np.int0(cv2.boxPoints(rect))
            
            cv2.drawContours(img, [box], -1, range_rgb[color_area_max], 2)
            if not start_pick_up:
                if color_area_max == 'red':  # 红色最大
                    color = 1
                elif color_area_max == 'green':  # 绿色最大
                    color = 2
                elif color_area_max == 'blue':  # 蓝色最大
                    color = 3
                elif color_area_max == 'gray':  # 蓝色最大
                    color = 4
                else:
                    color = 0
                color_list.append(color)
                if len(color_list) == 20:  # 多次判断
                    # 取平均值
                    color = int(round(np.mean(np.array(color_list))))
                    color_list = []
                    
                    if color == 1:
                        font_color = (0, 0, 255)                
                        detect_color = 'red'
                        set_rgb(detect_color)
                        garbage_species = 'Hazardous Waste'
                    elif color == 2:
                        font_color = (0, 255, 0)
                        detect_color = 'green'                      
                        set_rgb(detect_color)
                        garbage_species = 'Food Waste'
                    elif color == 3:
                        font_color = (255, 0, 0)
                        detect_color = 'blue'
                        set_rgb(detect_color)
                        garbage_species = 'Recyclable'
                    elif color == 4:
                        font_color = (50, 50, 50)
                        detect_color = 'gray'                        
                        set_rgb(detect_color)
                        garbage_species = 'Residual Waste'
                    else:
                        font_color = (0, 0, 0)
                        detect_color = 'None'
                        set_rgb(detect_color)
       
    cv2.putText(img, "Color: " + garbage_species, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, font_color, 2)
    return img

if __name__ == '__main__':
    initMove()
    cap = cv2.VideoCapture(-1) #读取摄像头
    __target_color = ('red', 'green', 'blue','gray')
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

        