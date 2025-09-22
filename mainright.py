# coding:utf-8
import math
import random

from kick_ball import kick_ball
from proxy_and_image import *
from recognized_ball import *

frameHeight = 0
frameWidth = 0
frameChannels = 0
frameArray = None
cameraPitchRange = 47.64 / 180 * math.pi
cameraYawRange = 60.97 / 180 * math.pi

row = "HeadPitch"
angle = 0.5235987755982988
maxstepx = 0.04
maxstepy = 0.11
maxsteptheta = 0.3
maxstepfrequency = 0.6
stepheight = 0.02
torsowx = 0.0
torsowy = 0.0


# 初始化函数
def initialize_robot(IP):
    AutonomousLifeProxy = get_Proxy("ALAutonomousLife", IP)
    AutonomousLifeProxy.setState("disabled")

    motionProxy = get_Proxy("ALMotion", IP)
    motionProxy.stiffnessInterpolation("Body", 1, 1)
    motionProxy.angleInterpolation(["HeadPitch", "HeadYaw"], [0, 0], [0.3, 0.3], True)

    postureProxy = get_Proxy("ALRobotPosture", IP)
    postureProxy.goToPosture("StandInit", 1.0)

    return motionProxy


# 视觉处理函数
def process_vision(vd_proxy, mt_proxy, config):
    videoClient = vd_proxy.subscribe("ball_" + str(random.random()), config["resolution"], config["colorSpace"],
                                     config["fps"])
    try:
        while True:
            img = get_image_from_camera(1, vd_proxy, videoClient)
            # 图像处理逻辑
            width = img.shape[1]
            height = img.shape[0]
            # 霍夫圆检测,返回结果为一个圆心的坐标(类型：tuple), 半径(类型double)
            cir_center, radius = detect_circle(img, config["white_low"], config["white_high"], config["black_low"],
                                               config["black_high"])
            print(cir_center, radius)
            # [0]为坐标x，[1]为坐标y
            if cir_center is not None:
                # 第一象限，球在左上方
                if height * 4 / 7 - cir_center[1] > 0:
                    print("向前走")
                    mt_proxy.moveTo(0.05, 0, 0)
                    if width / 2 - cir_center[0] > 0:
                        print("左")
                        mt_proxy.moveTo(0, 0.04, 0)
                    elif width * 3 / 4 - cir_center[0] < 0:
                        print("右")
                        mt_proxy.moveTo(0, -0.03, 0)
                elif width / 2 - cir_center[0] > 0 > height * 4 / 7 - cir_center[1]:
                    print("后退，左！")
                    mt_proxy.moveTo(-0.03, 0.03, 0)
                elif width * 3 / 4 - cir_center[0] < 0 and height * 4 / 7 - cir_center[1] < 0:
                    print("后退，右！")
                    mt_proxy.moveTo(-0.04, -0.04, 0)
                elif width / 2 - cir_center[0] < 0 and height * 4 / 7 - cir_center[1] < 0:
                    # mt_proxy.moveTo(0.01, 0.02, 0)
                    # hit_ball(ip)
                    kick_ball(mt_proxy)
                    # 第四象限，球在右脚下方，由于我们的预设程序是右脚踢球，执行踢球程序，并根据实际情况进行微调，
                    # cv2.imwrite方法保存下识别结果图片
                    mt_proxy.stiffnessInterpolation("Body", 1, 1)
                    mt_proxy.angleInterpolation(["HeadPitch", "HeadYaw"], [0, 0], [0.3, 0.3], True)

                    print("保存图片成功！")
                    cv2.imwrite("ball.jpg", img)
                    break
                else:
                    print('未知问题')
            # 未识别到足球的情况下，默认向前走
            else:
                mt_proxy.moveTo(0.09, 0, 0)
            cv2.imshow("res", img)
            cv2.waitKey(1)
            # 根据处理结果执行相应动作...
    finally:
        vd_proxy.unsubscribe(videoClient)
        print("ok")


# 主函数
def main():
    motionProxy = initialize_robot(CONFIG["ip"])

    # 执行其他任务...
    vd_proxy = get_Proxy("ALVideoDevice", CONFIG["ip"])
    process_vision(vd_proxy, motionProxy, CONFIG)

    kick_ball(motionProxy)

    print("完成任务")


if __name__ == '__main__':
    main()
