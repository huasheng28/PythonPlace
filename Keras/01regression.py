"""
回归
"""
# coding=utf-8
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt  # 可视化模块

# 设置随机种子，以便每次结果相同，可去除参数，则每次结果不同
np.random.seed(1337)  # for reproducibility

"""
准备数据
"""
# 创造从-1到1 ，个数200的数据
X = np.linspace(-1, 1, 200)
# 打乱排序
np.random.shuffle(X)
# 正态分布
Y = 0.5 * X + 2 + np.random.normal(0, 0.05, (200, ))
# 画图
plt.scatter(X, Y)
plt.show()
# 训练用数据集
X_train, Y_train = X[:160], Y[:160]     # train 前 160 data points
X_test, Y_test = X[160:], Y[160:]       # test 后 40 data points

"""
建立模型
"""
# 建立序贯模型
model = Sequential()
# 添加全链接神经层
model.add(Dense(output_dim=1, input_dim=1))

"""
激活模型
"""
# choose loss function and optimizing method
# 选择误差函数mse均方误差及优化器sgd随机梯度下降法
model.compile(loss='mse', optimizer='sgd')

"""
训练模型
"""
print('Training -----------')
for step in range(301):
    # 训练模型
    cost = model.train_on_batch(X_train, Y_train)
    if step % 100 == 0:
        print('train cost: ', cost)

"""
Training -----------
train cost:  4.111329555511475
train cost:  0.08777070790529251
train cost:  0.007415373809635639
train cost:  0.003544030711054802
"""

"""
检验模型
"""
print('\nTesting ------------')
# 函数按batch计算在某些输入数据上模型的误差
cost = model.evaluate(X_test, Y_test, batch_size=40)
print('test cost:', cost)
# 获取权重
W, b = model.layers[0].get_weights()
print('Weights=', W, '\nbiases=', b)

"""
Testing ------------
40/40 [==============================] - 0s
test cost: 0.004269329831
Weights= [[ 0.54246825]]
biases= [ 2.00056005]
"""

# 可视化结果
# 预测结果
Y_pred = model.predict(X_test)

plt.scatter(X_test, Y_test)
plt.plot(X_test, Y_pred)
plt.show()
