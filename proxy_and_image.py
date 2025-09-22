# coding:utf-8
import vision_definitions
from naoqi import ALProxy
import cv2
import numpy as np

# 配置参数
CONFIG = {
    "ip": "192.168.76.185",
    "resolution": vision_definitions.kVGA,
    "colorSpace": vision_definitions.kBGRColorSpace,
    "fps": 30,
    "white_low": [0, 4, 99],
    "white_high": [48, 255, 255],
    "black_low": [0, 0, 0],
    "black_high": [179, 255, 92],
    # 其他参数...
}


# 封装代理
def get_Proxy(modelName, IP, port=9559):
    proxy = ALProxy(modelName, IP, port)
    return proxy


def get_image_from_camera(camera_id, camera_proxy, videoClient):
    # 获取图片, 一帧一帧组成视频流
    camera_proxy.setActiveCamera(camera_id)

    # 返回的frame中， 第一维为图像的宽，第二维为图片的高，第三维为图片的通道数，第六维为图片本身数组
    frame = camera_proxy.getImageRemote(videoClient)
    frameWidth = frame[0]
    frameHeight = frame[1]
    frameChannels = frame[2]

    # 将图片转换成numpy数组，并且reshape成标准的形状，方便我们使用cv2来展示
    frameArray = np.frombuffer(frame[6], dtype=np.uint8).reshape([frameHeight, frameWidth, frameChannels])
    return frameArray


if __name__ == '__main__':
    vd_proxy = get_Proxy("ALVideoDevice", CONFIG["ip"])
    videoClient = vd_proxy.subscribeCamera("python_GVM", 1, CONFIG["resolution"], CONFIG["colorSpace"], CONFIG["fps"])
    while 1:
        img = get_image_from_camera(1, vd_proxy, videoClient)
        cv2.imshow("res", img)
        cv2.waitKey(1)
