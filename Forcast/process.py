# -*- coding: UTF-8 -*-

# -------------------------------------------------
#    请不要随意修改文件中的代码
# -------------------------------------------------


import sys
import time
import threading
import socket

CHARSET = "utf-8"  # 设置字符集（和PHP交互的字符集）

REQUEST_MIN_LEN = 10  # 合法的request消息包最小长度
TIMEOUT = 180  # socket处理时间180秒

pc_dict = {}  # 预编译字典，key:调用模块、函数、参数字符串，值是编译对象
global_env = {}  # global环境变量

# 深度学习预测
import numpy as np

from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications.resnet50 import ResNet50

img_width, img_height = 224, 256

# predict result file
output_file = '/root/Dande/keras/output/keras_result_51.txt'
# training weight path
weights_path = '/root/Dande/keras/output/weights_theano_51.hdf5'
# 梯度步长
batch_size = 1
# 50层残差网络模型，include_top：是否保留顶层的全连接网络，weights：None代表随机初始化，即不加载预训练权重
base_model = ResNet50(include_top=False, weights=None)

x = base_model.output
# 为空域信号施加全局平均值池化
x = GlobalAveragePooling2D()(x)
# 建立模型
predictions = Dense(51, activation='softmax')(x)
model = Model(input=base_model.input, output=predictions)
# 编译模型
model.compile(optimizer=SGD(lr=0.01,momentum=0.9,decay=1e-6),loss='categorical_crossentropy',metrics=['accuracy'])
# 从HDF5文件中加载权重到当前模型中
model.load_weights(weights_path)

# lock=threading.RLock()
def predict(items=None):
    image_num = 0
    while True:
        image_batch = []
        # 转换图片为PIL格式
        img = load_img(items, target_size=(img_width, img_height))
        # 图片转为数组
        image_batch.append(img_to_array(img))
        image_batch_num = len(image_batch)
        if image_batch_num % batch_size == 0:
            break
    image_num += len(image_batch)

    # 创建全零数组，uint8：无符号整数，0 至 255
    x_train = np.zeros(
        (len(image_batch),
         3,
         img_width,
         img_height),
        dtype="uint8")
    y_train = np.zeros(len(image_batch), dtype="uint8")

    # 列出索引序列，i为序号
    for i, img in enumerate(image_batch):
        x_train[i, :, :, :] = img
    # 图片生成器ImageDataGenerator：用以生成一个batch的图像数据，支持实时数据提升。训练时该函数会无限生成数据，直到达到规定的epoch次数为止。
    predict_datagen = ImageDataGenerator(rescale=1. / 255)
    # 接收numpy数组和标签为参数,生成经过数据提升或标准化后的batch数据,并在一个无限循环中不断的返回batch数据
    predict_gengerator = predict_datagen.flow(
        x_train, y_train, shuffle=False, batch_size=batch_size)

    # 从一个生成器上获取数据并进行预测
    result = model.predict_generator(predict_gengerator, batch_size)

    return result[0].argmax(), int(result[0].max() * 10000)


def index(bytes, c, pos=0):
    """
    查找c字符在bytes中的位置(从0开始)，找不到返回-1
    pos: 查找起始位置
    """
    for i in range(len(bytes)):
        if (i <= pos):
            continue
        if bytes[i] == c:
            return i
            break
    else:
        return -1


def z_encode(p):
    """
    encode param from python data
    """
    if p is None:  # None->PHP中的NULL
        return "N;"
    elif isinstance(p, int):  # int->PHP整形
        return "i:%d;" % p
    elif isinstance(p, str):  # String->PHP字符串
        p_bytes = p.encode(CHARSET)
        ret = 's:%d:"' % len(p_bytes)
        ret = ret.encode(CHARSET)
        ret = ret + p_bytes + '";'.encode(CHARSET)
        #ret = str(ret, CHARSET)
        ret = str(ret)
        return ret
    elif isinstance(p, bool):  # boolean->PHP布尔
        b = 1 if p else 0
        return 'b:%d;' % b
    elif isinstance(p, float):  # float->PHP浮点
        return 'd:%r;' % p
    elif isinstance(p, list) or isinstance(p, tuple):  # list,tuple->PHP数组(下标int)
        s = ''
        for pos, i in enumerate(p):
            s += z_encode(pos)
            s += z_encode(i)
        return "a:%d:{%s}" % (len(p), s)
    elif isinstance(p, dict):  # 字典->PHP数组(下标str)
        s = ''
        for key in p:
            s += z_encode(key)
            s += z_encode(p[key])
        return "a:%d:{%s}" % (len(p), s)
    else:  # 其余->PHP中的NULL
        return "N;"


def z_decode(p):
    """
    decode php param from string to python
    p: bytes
    """
    if p[0] == chr(0x4e):  # NULL 0x4e-'N'
        return None, p[2:]
    elif p[0] == chr(0x62):  # bool 0x62-'b'
        if p[2] == chr(0x30):                # 0x30-'0'
            return False, p[4:]
        else:
            return True, p[4:]
    elif p[0] == chr(0x69):  # int  0x69-'i'
        i = index(p, chr(0x3b), 1)           # 0x3b-';'
        return int(p[2:i]), p[i + 1:]
    elif p[0] == chr(0x64):  # double 0x64-'d'
        i = index(p, chr(0x3b), 1)           # 0x3b-';'
        return float(p[2:i]), p[i + 1:]
    elif p[0] == chr(0x73):  # string 0x73-'s'
        len_end = index(p, chr(0x3a), 2)     # 0x3a-':'
        str_len = int(p[2:len_end])
        end = len_end + 1 + str_len + 2
        v = p[(len_end + 2): (len_end + 2 + str_len)]
        # return str(v, CHARSET), p[end+1:]
        return v.encode(CHARSET), p[end + 1:]
    elif p[0] == chr(0x61):  # array 0x61-'a'
        list_ = []  # 数组
        dict_ = {}  # 字典
        flag = True  # 类型，true-元组 false-字典
        second = index(p, chr(0x3a), 2)      # 0x3a-":"
        num = int(p[2:second])  # 元素数量
        pp = p[second + 2:]  # 所有元素
        for i in range(num):
            key, pp = z_decode(pp)  # key解析
            if (i == 0):  # 判断第一个元素key是否int 0
                if (not isinstance(key, int)) or (key != 0):
                    flag = False
            val, pp = z_decode(pp)  # value解析
            list_.append(val)
            dict_[key] = val
        return (list_, pp[2:]) if flag else (dict_, pp[2:])
    else:
        return p, ''


def parse_php_req(p):
    """
    解析PHP请求消息
    返回：元组（模块名，函数名，入参list）
    """
    while p:
        v, p = z_decode(p)  # v：值  p：bytes(每次z_decode计算偏移量)
        params = v

    modul_func = params[0]  # 第一个元素是调用模块和函数名
    # print("模块和函数名:%s" % modul_func)
    # print("参数:%s" % params[1:])
    func = modul_func
    return func, params[1:]


class ProcessThread(threading.Thread):
    """
    preThread 处理线程
    """

    def __init__(self, socket):
        threading.Thread.__init__(self)

        # 客户socket
        self._socket = socket

    def run(self):

        #---------------------------------------------------
        #    1.接收消息
        #---------------------------------------------------

        try:
            self._socket.settimeout(TIMEOUT)  # 设置socket超时时间
            firstbuf = self._socket.recv(16 * 1024)  # 接收第一个消息包(bytes)
            if len(firstbuf) < REQUEST_MIN_LEN:  # 不够消息最小长度
                #print ("非法包，小于最小长度: %s" % firstbuf)
                print('error message,less than minimum length:', firstbuf)
                self._socket.close()
                return

            firstComma = index(firstbuf, chr(0x2c))  # 查找第一个","分割符
            #firstComma = index(firstbuf, ',')
            print(firstbuf)
            totalLen = int(firstbuf[0:firstComma])  # 消息包总长度
            #print("消息长度:%d" % totalLen)
            print('message length:', totalLen)
            reqMsg = firstbuf[firstComma + 1:]
            print('reqMsg:', reqMsg)
            while (len(reqMsg) < totalLen):
                reqMsg = reqMsg + self._socket.recv(16 * 1024)

            # 调试
            #print ("请求包：%s" % reqMsg)

        except Exception as e:
            #print ('接收消息异常', e)
            print('getMessage error', str(e))
            self._socket.close()
            return

        #---------------------------------------------------
        #    2.调用模块、函数检查，预编译。
        #---------------------------------------------------

        # 从消息包中解析出函数名、入参list
        func, params = parse_php_req(reqMsg)
        print('func:', func, 'parmas:', params)

        #---------------------------------------------------
        #    3.Python函数调用
        #---------------------------------------------------

        try:
            params = ','.join([repr(x) for x in params])
            print("调用函数及参数：%s(%s)" % (func, params))

            # strip前后端的“"”
            # print params.strip('\'')
            # 函数调用
            get_predict = getattr(sys.modules[__name__], func)
            pre_result = get_predict(params.strip('\''))

        except Exception as e:
            #print ('调用Python业务函数异常', e )
            print('call python error:', str(e))
            errType, errMsg, traceback = sys.exc_info()
            self._socket.sendall(("F%s" % errMsg).encode(CHARSET))  # 异常信息返回
            self._socket.close()
            return

        #---------------------------------------------------
        #    4.结果返回给PHP
        #---------------------------------------------------

        print(pre_result)
        rspStr = z_encode(pre_result)  # 函数结果组装为PHP序列化字符串
        print("函数结果组装为PHP序列化字符串：%s" % rspStr)

        print("- ")
        print("- 完成处理请求")
        print("- Time: %s" %time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        print("-------------------------------------------")

        try:
            # 加上成功前缀'S'
            rspStr = "S" + rspStr
            # 调试
            #print ("返回包：%s" % rspStr)
            self._socket.sendall(rspStr.encode(CHARSET))
        except Exception as e:
            print('send message error:', str(e))
            #print ('发送消息异常', e)
            errType, errMsg, traceback = sys.exc_info()
            self._socket.sendall(("F%s" % errMsg).encode(CHARSET))  # 异常信息返回
        finally:
            self._socket.close()
            return
