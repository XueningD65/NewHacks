#hash I am here
import wx
import wx.grid
import sqlite3
from time import localtime,strftime
import os
from skimage import io as iio
import io
import zlib
import dlib  # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import cv2  # 图像处理的库OpenCv
import _thread
import threading
import face_confirm as fc
import sql_login as sl
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog

facerec = dlib.face_recognition_model_v1("model/dlib_face_recognition_resnet_model_v1.dat")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    print("euclidean distance: ", dist)
    if dist > 0.4:
        return "diff"
    else:
        return "same"

def compare(name):
    cap = cv2.VideoCapture(0)
    im_fm = cv2.imread(sl.get_photo(name),0)
    dets_fm = detector(im_fm, 1)
    while cap.isOpened():
        # cap.read()
        # 返回两个值：
        #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
        #    图像对象，图像的三维矩阵
        flag, im_rd = cap.read()

        # 每帧数据延时1ms，延时为0读取的是静态帧
        kk = cv2.waitKey(1)
        # 人脸数 dets
        dets = detector(im_rd, 1)

        # 检测到人脸
        if len(dets) != 0:
            """
            biggest_face = dets[0]
            # 取占比最大的脸
            maxArea = 0
            for det in dets:
                w = det.right() - det.left()
                h = det.top() - det.bottom()
                if w * h > maxArea:
                    biggest_face = det
                    maxArea = w * h
                    # 绘制矩形框

            
            img_height, img_width = im_rd.shape[:2]
            image1 = cv2.cvtColor(im_rd, cv2.COLOR_BGR2RGB)
            pic = wx.Bitmap.FromBuffer(img_width, img_height, image1)
            # 显示图片在panel上
        ##    bmp.SetBitmap(pic)
            """
            cv2.rectangle(im_rd, tuple([dets[0].left(), dets[0].top()]),
                          tuple([dets[0].right(), dets[0].bottom()]),
                          (255, 0, 0), 2)

            # 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
            shape = predictor(im_rd, dets[0])
            features_cap = facerec.compute_face_descriptor(im_rd, shape)

            shape = predictor(im_fm,dets_fm[0])
            features_formal = facerec.compute_face_descriptor(im_fm, shape)

            # 对于某张人脸，遍历所有存储的人脸特征
            compare = return_euclidean_distance(features_cap, features_formal)
            if compare == "same":  # 找到了相似脸
                tkinter.messagebox.showinfo(title='face input', message='correct')
            else
                tkinter.messagebox.showinfo(title='face input', message='wrong')

            print(strftime("%Y-%m-%d %H:%M:%S",localtime())+" name "+name+"\r\n")

            """
            face_height = dets[0].bottom() - dets[0].top()
            face_width = dets[0].right() - dets[0].left()
            im_blank = np.zeros((face_height, face_width, 3), np.uint8)
            """
