# -*- coding: utf-8 -*-
import logging
import requests
import threading
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
import const
import time
import datetime
import psutil
import os
import win32api
import win32process
import csv


try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass
except Exception as err:
    raise err

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s  %(levelname)s %(message)s ',
    datefmt='%Y-%m-%d %A %H:%M:%S',
    filename='demo.log',
    filemode='a')
# console = logging.StreamHandler()                  # 定义console handler
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s  %(levelname)s  %(message)s')  # 定义该handler格式
# console.setFormatter(formatter)
# # Create an instance
# logging.getLogger().addHandler(console)  # 实例化添加handler


def execute(url, path, timeout, phone_list):
    now = datetime.datetime.now()
    try:
        r = requests.get(url=url, timeout=timeout, verify=False)
        resp_status = r.status_code
        logging.info(path + u"发送请求")
        print(now.strftime("%Y.%m.%d-%H:%M:%S ") + path + u"发送请求")
        if resp_status != 200:
            do_send(phone_list)
            kill_and_start(path)
            logging.warning(path + u"返回失败")
            print(now.strftime("%Y.%m.%d-%H:%M:%S ") + path + u"返回失败")
    except requests.exceptions.ConnectTimeout:
        do_send(phone_list)
        kill_and_start(path)
        logging.error(path + u"连接超时")
        print(now.strftime("%Y.%m.%d-%H:%M:%S ") + path + u"连接超时")
    except requests.exceptions.ConnectionError:
        do_send(phone_list)
        kill_and_start(path)
        logging.error(path + u"连接错误")
        print(now.strftime("%Y.%m.%d-%H:%M:%S ") + path + u"连接错误")
    except requests.exceptions.Timeout:
        do_send(phone_list)
        kill_and_start(path)
        logging.error(path + u"请求超时")
        print(now.strftime("%Y.%m.%d-%H:%M:%S ") + path + u"请求超时")


def ali_send(
        business_id,
        phone_numbers,
        sign_name,
        template_code,
        template_param=None):
    # 阿里云短信发送
    REGION = u"cn-hangzhou"
    PRODUCT_NAME = u"Dysmsapi"
    DOMAIN = u"dysmsapi.aliyuncs.com"
    acs_client = AcsClient(
        const.ACCESS_KEY_ID,
        const.ACCESS_KEY_SECRET,
        REGION)
    region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)
    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)
    # 短信签名
    smsRequest.set_SignName(sign_name)
    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)
    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    return smsResponse


def do_send(phone_list):
    # 短信发送参数
    __business_id = uuid.uuid1()
    # phone_numbers = u"18025093565"
    sign_name = u"阿里云短信测试专用"
    template_code = u"SMS_130550008"
    params = u"{\"code\":\"12345\"}"
    for phone_number in phone_list:
        ali_send(__business_id, phone_number, sign_name, template_code, params)
    # logging.info(resp)
    # pass


class my_thread(threading.Thread):
    # 重写线程
    def __init__(self, url, path, timeout, phone_list):
        threading.Thread.__init__(self)
        self.url = url
        self.path = path
        self.timeout = timeout
        self.phone_list = phone_list

    def run(self):
        execute(self.url, self.path, self.timeout, self.phone_list)


def start_thread(url, path, timeout, phone_list):
    # 开启线程
    now = datetime.datetime.now()
    try:
        my_thread(url, path, timeout, phone_list).start()
    except BaseException:
        logging.warning(path + u"创建线程失败")
        print(now.strftime("%Y.%m.%d-%H:%M:%S ") + path + u"创建线程失败")


def kill_and_start(path):
    # 重启程序
    for i in psutil.process_iter():
        if i.name() == 'tusin.exe':
            if i.exe() == path:
                i.kill()
    # os.system(path)
    win32api.ShellExecute(0, 'open', path, '', '', 1)
    # win32process.CreateProcess(path, '', None, None, 0, win32process.CREATE_NEW_CONSOLE, None, None,win32process.STARTUPINFO())


def read_csv_file():
    with open('data.csv', 'rb') as f:
        reader = csv.reader(f)
        for i, rows in enumerate(reader):
            if i == 0:
                out_time_list = rows
            if i == 1:
                delay_time_list = rows
            if i == 2:
                phone_list = rows
            if i == 3:
                url_list = rows
            if i == 4:
                path_list = rows
    # 超时时间
    outtime = out_time_list[0]
    # 循环时间
    delaytime = delay_time_list[0]

    return outtime, delaytime, phone_list, url_list, path_list


if __name__ == '__main__':
    out_time, delay_time, phone_list, url_list, path_list = read_csv_file()

    while True:
        for (a, b) in zip(url_list, path_list):
            start_thread(a, b, float(out_time), phone_list)
        time.sleep(float(delay_time))
