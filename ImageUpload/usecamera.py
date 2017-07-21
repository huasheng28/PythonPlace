#coding=utf-8
import os,time
i=0
#RENMI
# for i in range(1000):
#     #点击按钮
#     os.system("adb shell input touchscreen tap 540 1491")
#     time.sleep(1)
#     #点击相机
#     os.system("adb shell input touchscreen tap 200 1490")
#     time.sleep(1)
#     #点击拍照
#     os.system("adb shell input touchscreen tap 540 1809")
#     time.sleep(3)
#     #点击上传
#     os.system("adb shell input touchscreen tap 852 1738")
#     time.sleep(2)
#     #点击返回
#     os.system("adb shell input touchscreen tap 540 1738")
#     time.sleep(1)
#     i=i+1
#     print(i)
#VIVO
for i in range(1000):
    #点击按钮
    os.system("adb shell input touchscreen tap 648 1493")
    time.sleep(1)
    #点击相机
    os.system("adb shell input touchscreen tap 168 1460")
    time.sleep(1)
    #点击拍照
    os.system("adb shell input touchscreen tap 600 1822")
    time.sleep(3)
    #点击上传
    os.system("adb shell input touchscreen tap 969 1771")
    time.sleep(3)
    #点击返回
    os.system("adb shell input touchscreen tap 679 1718")
    time.sleep(1)
    i=i+1
    print(i)