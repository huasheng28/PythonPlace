#coding=utf-8
import time
from selenium import webdriver
def circle():
    i=0
    j=0
    driver=webdriver.Chrome()
    driver.get("http://test.seeunsee.cn/jsb/wm-test")
    time.sleep(5)
    for _ in range(10000):
        driver.find_element_by_name("file").send_keys("C:\Users\Administrator\Pictures\Saved Pictures\pian.jpg")
        time.sleep(5)
        zi = driver.find_element_by_id("hint-progress").text
        if zi==u"正在核查...":
            time.sleep(5)
            zi = driver.find_element_by_id("hint-progress").text
            if zi == u"正在核查...":
                time.sleep(5)
                zi = driver.find_element_by_id("hint-progress").text
                if zi==u"正在核查...":
                    time.sleep(5)
                    zi = driver.find_element_by_id("hint-progress").text
                    if zi == u"正在核查...":
                        j = j + 1
                        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    else:
                        i = i + 1
                else:
                    i=i+1
            else:
                i = i + 1
        else:
            i=i+1
        print i+j,j
        driver.find_element_by_id("btnCancel").click()
circle()