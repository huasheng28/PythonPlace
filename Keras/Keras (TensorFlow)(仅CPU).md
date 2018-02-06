# Keras (TensorFlow)(仅CPU)

## 环境配置
* win10
* Python环境：
安装Anaconda Anaconda2 for Python2,Anaconda3 for Python3
推荐Anconda3 4.2.0，目前新出的python3.6存在部分不兼容问题，windows版本下的tensorflow暂时不支持python2.7
[下载地址](https://repo.continuum.io/archive/index.html)
* CMD
```
# 升级TensorFlow，如果出现setuptools相关问题，执行conda update setuptools
pip install --upgrade tensorflow

# Keras 安装
pip install keras -U --pre

# 验证安装
python
import keras
#无报错则安装成功
```
* Keras中mnist数据集测试 下载Keras开发包
```
conda install git
git clone https://github.com/fchollet/keras.git
cd keras/examples/
python mnist_mlp.py
# 可能发生网络错误
```
