"""
分类神经网络
"""
# coding=utf-8
# mnist数据集分为训练集和测试集
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import RMSprop
import numpy as np

"""
数据预处理
"""
# download the mnist to the path '~/.keras/datasets/' if it is the first time to be called
# X shape (60,000 28x28), y shape (10,000, )
# x 是一张张图片，y 是每张图片对应的标签，即它是哪个数字
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# 输入的 x 变成 60,000*784 的数据，然后除以 255 进行标准化，因为每个像素都是在 0 到 255 之间的，标准化之后就变成了 0
# 到 1 之间。
X_train = X_train.reshape(X_train.shape[0], -1) / 255.
X_test = X_test.reshape(X_test.shape[0], -1) / 255.
# 把 y 变成了 one-hot 的形式，即之前 y 是一个数值， 在 0-9 之间，现在是一个大小为 10
# 的向量，它属于哪个数字，就在哪个位置为 1，其他位置都是 0。
y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

print(X_train[1].shape)
"""
(784,)
"""

print(y_train[:3])
"""
[[ 0.  0.  0.  0.  0.  1.  0.  0.  0.  0.]
 [ 1.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  1.  0.  0.  0.  0.  0.]]
"""

"""
建立神经网络
"""
"""
models.Sequential，用来一层一层一层的去建立神经层；
layers.Dense 意思是这个神经层是全连接层。
layers.Activation 激励函数。
optimizers.RMSprop 优化器采用 RMSprop，加速神经网络训练方法。
"""

np.random.seed(1337)  # for reproducibility

# Another way to build your neural net
model = Sequential([
    # 加入 Dense 神经层。32 是输出的维度，784 是输入的维度。 第一层传出的数据有 32 个 feature，传给激励单元
    Dense(32, input_dim=784),
    # 激励函数用到的是 relu 函数。 经过激励函数之后，就变成了非线性的数据。 然后再把这个数据传给下一个神经层
    Activation('relu'),
    # 这个 Dense 我们定义它有 10 个输出的 feature。同样的，此处不需要再定义输入的维度，因为它接收的是上一层的输出。
    Dense(10),
    #  接下来再输入给下面的 softmax 函数，用来分类
    Activation('softmax'),
])

# 用 RMSprop 作为优化器，它的参数包括学习率等
# Another way to define your optimizer
rmsprop = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

# 优化器，可以是默认的，也可以是我们在上一步定义的。 损失函数，分类和回归问题的不一样，用的是交叉熵。 metrics，里面可以放入需要计算的 cost，accuracy，score 等
# We add metrics to get more results you want to see
model.compile(optimizer=rmsprop,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

"""
训练网络
"""
print('Training ------------')
# Another way to train the model
#  fit 函数，把训练集的 x 和 y 传入之后，nb_epoch 表示把整个数据训练多少次，batch_size 每批处理32个。
model.fit(X_train, y_train, epoch=2, batch_size=32)

"""
Training ------------
Epoch 1/2
60000/60000 [==============================] - 2s - loss: 0.3506 - acc: 0.9025
Epoch 2/2
60000/60000 [==============================] - 2s - loss: 0.1995 - acc: 0.9421
"""

"""
测试模型
"""
print('\nTesting ------------')
# Evaluate the model with the metrics we defined earlier
loss, accuracy = model.evaluate(X_test, y_test)

print('test loss: ', loss)
print('test accuracy: ', accuracy)

"""
Testing ------------
 9760/10000 [============================>.] - ETA: 0s

test loss:  0.1724540345
test accuracy:  0.9489
"""
