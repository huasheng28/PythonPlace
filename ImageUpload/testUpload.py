#utf-8
import threading
from time import ctime
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
i=0
for i in range(1):
    register_openers()
    datagen, headers = multipart_encode({"file": open("pian1.jpg", "rb")})
    request = urllib2.Request("http://test.seeunsee.cn/jsb/wm-test/api/check.php", datagen, headers)
    i+=1
    print urllib2.urlopen(request).read(),i