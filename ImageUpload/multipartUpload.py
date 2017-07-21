#coding=utf-8
import threading
from time import ctime
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
def one(cishu):
    a = 0
    register_openers()
    datagen, headers = multipart_encode({"file": open("pian1.jpg", "rb")})
    request = urllib2.Request("http://test.seeunsee.cn/jsb/wm-test/api/check.php", datagen, headers)
    a += 1
    print urllib2.urlopen(request).read(),ctime(), "a",a
def two(cishu):
    b = 0
    register_openers()
    datagen, headers = multipart_encode({"file": open("pian2.jpg", "rb")})
    request = urllib2.Request("http://test.seeunsee.cn/jsb/wm-test/api/check.php", datagen, headers)
    b += 1
    print urllib2.urlopen(request).read(), ctime(),"b", b
def three(cishu):
    c = 0
    register_openers()
    datagen, headers = multipart_encode({"file": open("pian3.jpg", "rb")})
    request = urllib2.Request("http://test.seeunsee.cn/jsb/wm-test/api/check.php", datagen, headers)
    c += 1
    print urllib2.urlopen(request).read(), ctime(),"c", c
threads=[]
t1=threading.Thread(target=one(1))
threads.append(t1)
t2 = threading.Thread(target=two(1))
threads.append(t2)
t3 = threading.Thread(target=three(1))
threads.append(t3)
def circle():
    for t in threads:
        t.setDaemon(True)
        t.start()
    print "all over %s" %ctime()