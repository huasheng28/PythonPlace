#coding=utf-8
import os,time
i=0
for i in range(100):
    #点击按钮
    os.system("adb shell input touchscreen tap 552 1541")
    time.sleep(1)
    #点击相册
    os.system("adb shell input touchscreen tap 436 1492")
    time.sleep(2)
    #点击图片
    os.system("adb shell input touchscreen tap 134 1008")
    time.sleep(5)
    #点击取消
    os.system("adb shell input touchscreen tap 528 1217")
    time.sleep(1)
    i=i+1
    print(i)