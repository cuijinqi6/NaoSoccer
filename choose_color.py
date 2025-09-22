# coding:utf-8

# 掩膜操作
import numpy as np
import cv2
from recognized_ball import *
from main import *
# 0 179 41 255 41 255
def empty(a):
    pass
print("Package Imported")
# 导入图片
path = "./soccer.jpg"
def choose_color_1():
    # 滑动条
    # 创建一个新的窗口来存放滑动条
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 240)
    # 这里以HSV为示例， 三通道一共六个参数，分别为三通道的最小值，最大值， empty为回调函数
    # 第五个参数是回调函数，每次滑动条的滑动都会调用回调函数。回调函数通常会有一个默认参数，就是滑动条的位置。
    cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

    while True:
        img = cv2.imread(path)
        imgRe = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        imgHSV = cv2.cvtColor(imgRe, cv2.COLOR_BGR2HSV)
        h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
        s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
        print(h_min, h_max, s_min, s_max, v_min, v_max)
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        # 掩膜操作,设置区间,仅保留lower与upper之间的颜色
        mask = cv2.inRange(imgHSV, lower, upper)

        # 逻辑与
        imgResult = cv2.bitwise_and(imgRe, imgRe, mask=mask)
        cv2.imshow("Output", imgRe)
        cv2.imshow("Output1", imgHSV)
        cv2.imshow("mask",mask)
        cv2.imshow("mask",imgResult)
        cv2.waitKey(1)






    # 组合两个二值图
def contist(img1, img2):
    res = img1 + img2
    for i in res:
        for j in i:
            if j > 1:
                j = 1
    return res

if __name__ == '__main__':
    img = cv2.imread(path)
    # cap = cv2.VideoCapture(0)
    # while 1:
    #     success, img = cap.read()
    res1 = recognized_toBytes(img, white_low, white_high)
    res2 = recognized_toBytes(img, black_low, black_high)
    res = contist(res1, res2)
    cv2.imshow("res", res)
    cv2.waitKey(0)
    # choose_color_1()
