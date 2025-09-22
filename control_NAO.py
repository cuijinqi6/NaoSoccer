# coding:utf-8

from proxy_and_image import *
# 移动角度
def change_the_postion(mt_proxy, name, targetAngles):
    mt_proxy.angleInterpolationWithSpeed(name, targetAngles, 0.2)
    return True


if __name__ == '__main__':
    ip = "192.168.43.177"
    mt_proxy = get_Proxy("ALMotion", ip)
    mt_proxy.moveTo(0.4, 0, 0)

