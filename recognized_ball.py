# coding:utf-8

from proxy_and_image import *
import cv2
import numpy as np


def preprocess_image(bgr_img, arr1, arr2, arr3, arr4):
    """
    对图像进行预处理，包括HSV转换，颜色过滤，平滑处理，腐蚀和膨胀
    """
    # 转换为HSV
    hue_image = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

    # 颜色分割
    low_range = np.array(arr1)
    high_range = np.array(arr2)
    low_range2 = np.array(arr3)
    high_range2 = np.array(arr4)

    mask1 = cv2.inRange(hue_image, low_range, high_range)
    mask2 = cv2.inRange(hue_image, low_range2, high_range2)
    combined_mask = cv2.add(mask1, mask2)

    # 平滑处理
    gaus = cv2.GaussianBlur(combined_mask, (7, 7), 1.5)

    # 腐蚀和膨胀
    eroded = cv2.erode(gaus, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)), iterations=2)
    dilated = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)

    return dilated


def detect_circle(bgr_img, arr1, arr2, arr3, arr4):
    """
    检测图像中的圆形物体
    """
    preprocessed_image = preprocess_image(bgr_img, arr1, arr2, arr3, arr4)

    # 霍夫圆检测
    circles = cv2.HoughCircles(preprocessed_image, cv2.HOUGH_GRADIENT, 1, 100, param1=15, param2=7, minRadius=15,
                               maxRadius=100)

    if circles is not None:
        # 仅取最大的一个圆
        x, y, radius = circles[0][0]
        center = (x, y)
        cv2.circle(bgr_img, center, radius, (0, 255, 0), 2)
        return center, radius
    else:
        return None, None


def main():
    cap = cv2.VideoCapture(0)

    try:
        while True:
            success, img = cap.read()
            if not success:
                break

            center, radius = detect_circle(img, CONFIG["white_low"], CONFIG["white_high"], CONFIG["black_low"],
                                           CONFIG["black_high"])
            if center is not None:
                print("Detected circle at {} with radius {}".format(center, radius))

            cv2.imshow("res", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
