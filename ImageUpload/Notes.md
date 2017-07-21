Seleium Notes
##浏览器操作
* 浏览器最大化
```python
from seleium import webdriver
driver=webdriver.Chrome()
driver.get("http://www.baidu.com")
driver.maximize_window()
```
* 设置浏览器宽高
```
driver.set_window_size(400,800)
```
* 浏览器前进后退
```
driver.back()
driver.foward()
```
##对象的定位
* 元素定位
```
find_element_by_id()
find_element_by_name()
find_element_by_class_name()
find_element_by_tag_name()
find_element_by_link_text()
find_element_by_partial_link_text()
find_element_by_xpath()
find_element_by_css_selector()
```
## 操作测试对象
* 基本方法
clear()
send_keys(u"中文内容")
click()
submit()
* webelement接口常用方法
```
#返回百度输入框宽高
size=driver.find_element_by_id("kw").size
print size
#返回百度页面底部备案信息
text=driver.find_element_by_id("cp").text
print text
#返回元素的属性值，可以是 id、name、type 或元素拥有的其它任意属性
attribute=driver.find_element_by_id("kw").get_attribute('type')
print attribute
#返回元素的结果是否可见，返回结果为 True 或 False
result=driver.find_element_by_id("kw").is_displayed()
print result
```
##鼠标事件
* 鼠标操作常用方法
context_click() 右击
double_click() 双击
drag_and_drop() 拖动
move_to_element() 鼠标悬停在一个元素上
click_and_hold() 按下鼠标左键在一个元素上
context_click() 右键点击一个元素
```
#引入 ActionChains 类
from selenium.webdriver.common.action_chains import ActionChains
...
#定位到要右击的元素
right =driver.find_element_by_xpath("xx")
#对定位到的元素执行鼠标右键操作
ActionChains(driver).context_click(right).perform()
```
##键盘事件
```
#coding=utf-8
from selenium import webdriver
#引入 Keys 类包
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
#输入框输入内容
driver.find_element_by_id("kw").send_keys("selenium")
#删除多输入的一个 m
driver.find_element_by_id("kw").send_keys(Keys.BACK_SPACE)
#输入空格键+“教程”
driver.find_element_by_id("kw").send_keys(Keys.SPACE)
driver.find_element_by_id("kw").send_keys(u"教程")
#ctrl+a 全选输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'a')
#ctrl+x 剪切输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'x')
#输入框重新输入内容，搜索
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'v')
#通过回车键盘来代替点击操作
driver.find_element_by_id("su").send_keys(Keys.ENTER)
```
## 设置等待时间
sleep()：设置固定休眠时间。python 的 time 包提供了休眠方法 sleep() ，导入 time 包后就可以使用 sleep()进行脚本的执行过程进行休眠。
implicitly_wait()：是 webdirver提供的一个超时等待。等待一个元素被发现，或一个命令完成。如果超出了设置时间的则抛出异常。
WebDriverWait()：同样也是webdirver提供的方法。在设置时间内，默认每隔一段时间检测一次当前页面元素是否存在，如果超过设置时间检测不到则抛出异常。
```
from selenium import webdriver
#导入 WebDriverWait 包
from selenium.webdriver.support.ui import WebDriverWait
#导入 time 包
import time
driver = webdriver.Firefox()
driver.get("http://www.baidu.com")
#WebDriverWait()方法使用
element=WebDriverWait(driver, 10).until(lambda driver :driver.find_element_by_id("kw"))
element.send_keys("selenium")
#添加智能等待
driver.implicitly_wait(30)
driver.find_element_by_id("su").click()
#添加固定休眠时间
time.sleep(5)
driver.quit()
```
## 定位一组对象
```
from selenium import webdriver
import os
driver = webdriver.Firefox()
file_path = 'file:///' + os.path.abspath('checkbox.html')
driver.get(file_path)
# 选择页面上所有的 tag name 为 input 的元素
inputs = driver.find_elements_by_tag_name('input')
#然后从中过滤出 tpye 为 checkbox 的元素，单击勾选
for input in inputs:
    if input.get_attribute('type') == 'checkbox':
        input.click()
driver.quit()
```
```
#coding=utf-8
from selenium import webdriver
import os
driveriver = webdriver.Firefox()
file_path = 'file:///' + os.path.abspath('checkbox.html')
driver.get(file_path)
# 选择所有的 type 为 checkbox 的元素并单击勾选
checkboxes = driver.find_elements_by_css_selector('input[type=checkbox]')
for checkbox in checkboxes:
    checkbox.click()
# 打印当前页面上 type 为 checkbox 的个数
print len(driver.find_elements_by_css_selector('input[type=checkbox]'))
# 把页面上最后1个 checkbox 的勾给去掉
driver.find_elements_by_css_selector('input[type=checkbox]').pop().click()
driver.quit()
```
##定位 frame 中的对象
switch_to_frame 方法可以把当前定位的主体切换了 frame里。怎么理解这句话呢？我们可以从frame的实质去理解。frame 中实际上是嵌入了另一个页面，而 webdriver 每次只能在一个页面识别，因此才需要用 switch_to.frame 方法去获取 frame中嵌入的页面，对那个页面里的元素进行定位。
```
#先找到到 ifrome1（id = f1）
driver.switch_to_frame("f1")
#再找到其下面的 ifrome2(id =f2)
driver.switch_to_frame("f2")
```
switch_to_frame 的参数问题。官方说 name 是可以的，但是经过实验发现 id 也可以
##对话框处理
二次定位
```
#coding=utf-8
from selenium import webdriver
driver = webdriver.Firefox()
driver.get("http://www.baidu.com/")
#点击登录链接
driver.find_element_by_name("tj_login").click()
#通过二次定位找到用户名输入框
div=driver.find_element_by_class_name("tang-content").find_element_by_name("userName")
div.send_keys("username")
#输入登录密码
driver.find_element_by_name("password").send_keys("password")
#点击登录
driver.find_element_by_id("TANGRAM__PSP_10__submit").click()
driver.quit()
```
##浏览器多窗口处理
```
#coding=utf-8
from selenium import webdriver
import time
driver = webdriver.Firefox()
driver.get("http://www.baidu.com/")
#获得当前窗口
nowhandle=driver.current_window_handle
#打开注册新窗口
driver.find_element_by_name("tj_reg").click()
#获得所有窗口
allhandles=driver.window_handles
#循环判断窗口是否为当前窗口
for handle in allhandles:
    if handle != nowhandle:
    driver.switch_to_window(handle)
    print 'now register window!'
    #切换到邮箱注册标签
    driver.find_element_by_id("mailRegTab").click()
    time.sleep(5)
    driver.close()
#回到原先的窗口
driver.switch_to_window(nowhandle)
driver.find_element_by_id("kw").send_keys(u"注册成功！")
time.sleep(3)
driver.quit()
```
方法：
current_window_handle  获得当前窗口句柄
window_handles  返回的所有窗口的句柄到当前会话
switch_to_window()
用于处理多窗口操作的方法，与我们前面学过的 switch_to_frame() 是类似，switch_to_window()用于
处理多窗口之前切换，switch_to_frame() 用于处理多框架的切换。
close()
如果你足够细心会发现我们在关闭“注册页”时用的是 close()方法，而非 quit()；close()用于关闭当前
窗口，quit()用于退出驱动程序并关闭所有相关窗口。
##alert/confirm/prompt 处理
```
#coding=utf-8
from selenium import webdriver
import time
driver = webdriver.Firefox()
driver.get("http://www.baidu.com/")
#点击打开搜索设置
driver.find_element_by_name("tj_setting").click()
driver.find_element_by_id("SL_1").click()
#点击保存设置
driver.find_element_by_xpath("//div[@id='gxszButton']/input").click()
#获取网页上的警告信息
alert=driver.switch_to_alert()
#接收警告信息
alert.accept()
#得到文本信息并打印
alert = driver.switch_to_alert()
print alert.text()
#取消对话框（如果有的话）
alert = driver.switch_to_alert()
alert.dismiss()
#输入值（如果有的话）
alert = driver.switch_to_alert()
alert.send_keys(“xxx”)
```
##调用 JavaScript
* 执行 js 一般有两种场景：
1. 一种是在页面上直接执行 JS
2. 另一种是在某个已经定位的元素上执行 JS
```
#coding=utf-8
from selenium import webdriver
import time,os
driver = webdriver.Firefox()
file_path = 'file:///' + os.path.abspath('js.html')
driver.get(file_path)
#通过 JS 隐藏选中的元素第一种方法：
#隐藏文字信息
driver.execute_script('$("#tooltip").fadeOut();')
time.sleep(5)
#隐藏按钮：
button = driver.find_element_by_class_name('btn')
driver.execute_script('$(arguments[0]).fadeOut()',button)
time.sleep(5)
```
* execute_script(script, *args)
在当前窗口/框架 同步执行 javaScript
script：JavaScript 的执行。
*args：适用任何 JavaScript 脚本
##控制浏览器滚动条
* 用于标识滚动条位置的代码
```
<body onload= "document.body.scrollTop=0 ">
<body onload= "document.body.scrollTop=100000 ">
```
```
from selenium import webdriver
import time
#访问百度
driver=webdriver.Firefox()
driver.get("http://www.baidu.com")
#搜索
driver.find_element_by_id("kw").send_keys("selenium")
driver.find_element_by_id("su").click()
time.sleep(3)
#将页面滚动条拖到底部
js="var q=document.documentElement.scrollTop=10000"
driver.execute_script(js)
time.sleep(3)
#将滚动条移动到页面的顶部
js_="var q=document.documentElement.scrollTop=0"
driver.execute_script(js_)
time.sleep(3)
driver.quit()
```
##cookie 处理
* webdriver 操作 cookie 的方法有：
get_cookies() 获得所有 cookie 信息
get_cookie(name) 返回特定 name 有 cookie 信息
add_cookie(cookie_dict) 添加 cookie，必须有 name 和 value 值
delete_cookie(name) 删除特定(部分)的 cookie 信息
delete_all_cookies() 删除所有 cookie 信息
```
#coding=utf-8
from selenium import webdriver
import time
driver = webdriver.Firefox()
driver.get("http://www.youdao.com")
#向 cookie 的 name 和 value 添加会话信息。
driver.add_cookie({'name':'key-aaaaaaa', 'value':'value-bbbb'})
#遍历 cookies 中的 name 和 value 信息打印，当然还有上面添加的信息
for cookie in driver.get_cookies():
print "%s -> %s" % (cookie['name'], cookie['value'])
##### 下面可以通过两种方式删除 cookie #####
# 删除一个特定的 cookie
driver.delete_cookie("CookieName")
# 删除所有 cookie
driver.delete_all_cookies()
time.sleep(2)
driver.close()
```
##获取对象的属性
获取测试对象的属性能够帮我们更好的进行对象的定位。比如页面上有很多标签为 input 元素，而我
们需要定位其中 1 个有具有 data-node 属性不一样的元素。由于 webdriver 是不支持直接使用 data-node 来
定位对象的，所以我们只能先把所有标签为 input 都找到，然后遍历这些 input，获取想要的元素
```
<input type="checkbox" data-node="594434499" data-convert="1" data-type="file">
<input type="checkbox" data-node="594434498" data-convert="1" data-type="file">
<input type="checkbox" data-node="594434493" data-convert="1" data-type="file">
<input type="checkbox" data-node="594434497" data-convert="1" data-type="file">
```
```
# 选择页面上所有的 tag name 为 input 的元素
inputs = driver.find_elements_by_tag_name('input')
#然后循环遍历出 data-node 为594434493的元素，单击勾选
for input in inputs:
    if input.get_attribute('data-node') == '594434493':
        input.click()
```
##验证码问题
* 去掉验证码
* 设置万能码
* 验证码识别技术Python-tesseract
* 记录 cookie
```
#访问 xxxx 网站
driver.get("http://www.xxxx.cn/")
#将用户名密码写入浏览器 cookie
driver.add_cookie({'name':'Login_UserNumber', 'value':'username'})
driver.add_cookie({'name':'Login_Passwd', 'value':'password'})
#再次访问 xxxx 网站，将会自动登录
driver.get("http://www.xxxx.cn/")
```
使用 cookie 进行登录最大的难点是如何获得用户名密码的 name ，如果找到不到 name 的名字，就没
办法向 value 中输用户名、密码信息。
建议可以通过 get_cookies()方法来获取登录的所有的 cookie 信息，从而进行找到用户名、
密码的 name 对象的名字；当然，最简单的方法还是询问前端开发人员
##数据驱动（参数化）
```
#coding=utf-8
from selenium import webdriver
import os,time
source = open("F:\Code\seleium-test\data.txt", "r")
values = source.readlines()
source.close()
# 执行循环
driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
for serch in values:
    driver.find_element_by_id("kw").send_keys(serch)
    driver.find_element_by_id("su").click()
    time.sleep(3)
    driver.find_element_by_id("kw").clear()
driver.quit()
```
```
#coding=utf-8
import csv #导入 csv 包
#读取本地 CSV 文件
my_file='D:\\selenium_python\\data\\userinfo.csv'
data=csv.reader(file(my_file,'rb'))
#循环输出每一行信息
for user in data:
    print user[0]
    print user[1]
    print user[2]
    print user[3]
```
##异常断言
```
try:
    open("abc.txt",'r')
except IOError:
    pass
```
```
#打印错误信息
try:
    print aa
except NameError, msg:
    print msg
```
* Try...finally...子句用来表达这样的情况：
我们不管线捕捉到的是什么错误，无论错误是不是发生，这些代码“必须”运行，比如文件关闭，释放锁，把数据库连接返还给连接池等
```
import time
try:
    f = file('poem.txt')
    while True: # our usual file-reading idiom
        line = f.readline()
        if len(line) == 0:
            break
        time.sleep(2)
        print line,
finally:
    f.close()
    print 'Cleaning up...closed the file'
```
* Raise 抛出异常
```
#coding=utf-8
filename = raw_input('please input file name:')
if filename=='hello':
    raise NameError('input file name error !')
```
##weddriver 错误截图
```
#coding=utf-8
from selenium import webdriver
browser = webdriver.Firefox()
browser.get("http://www.baidu.com")
#捕捉百度输入框异常
try:
    browser.find_element_by_id("kwsss").send_keys("selenium")
    browser.find_element_by_id("su").click()
except:
    browser.get_screenshot_as_file("/home/fnngj/python/error_png.png")
    browser.quit()
```