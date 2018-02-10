import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import SimpleRNN, Activation, Dense
from keras.optimizers import Adam

TIME_STEPS = 28     # same as the height of the image
INPUT_SIZE = 28     # same as the width of the image
BATCH_SIZE = 50
BATCH_INDEX = 0
OUTPUT_SIZE = 10
CELL_SIZE = 50
LR = 0.001


# download the mnist to the path '~/.keras/datasets/' if it is the first time to be called
# X shape (60,000 28x28), y shape (10,000, )
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# data pre-processing
"""
MNIST里面的图像分辨率是28×28，为了使用RNN，我们将图像理解为序列化数据。 每一行作为一个输入单元，所以输入数据大小INPUT_SIZE = 28； 
先是第1行输入，再是第2行，第3行，第4行，…，第28行输入， 这就是一张图片也就是一个序列，所以步长TIME_STEPS = 28。
训练数据要进行归一化处理，因为原始数据是8bit灰度图像所以需要除以255。
"""
X_train = X_train.reshape(-1, 28, 28) / 255.      # normalize
X_test = X_test.reshape(-1, 28, 28) / 255.        # normalize
y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

# build RNN model
model = Sequential()

# RNN cell
# 输入为训练数据，输出数据大小由CELL_SIZE定义
model.add(SimpleRNN(
    # for batch_input_shape, if using tensorflow as the backend, we have to put None for the batch_size.
    # Otherwise, model.evaluate() will get error.
    batch_input_shape=(None, TIME_STEPS, INPUT_SIZE),       # Or: input_dim=INPUT_SIZE, input_length=TIME_STEPS,
    output_dim=CELL_SIZE,
    unroll=True,
))

# output layer
# 然后添加输出层，激励函数选择softmax
model.add(Dense(OUTPUT_SIZE))
model.add(Activation('softmax'))

# optimizer
# 设置优化方法，loss函数和metrics方法之后就可以开始训练了。
# 每次训练的时候并不是取所有的数据，只是取BATCH_SIZE个序列，或者称为BATCH_SIZE张图片，这样可以大大降低运算时间，提高训练效率
adam = Adam(LR)
model.compile(optimizer=adam,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# training
for step in range(4001):
    # data shape = (batch_num, steps, inputs/outputs)
    X_batch = X_train[BATCH_INDEX: BATCH_INDEX + BATCH_SIZE, :, :]
    Y_batch = y_train[BATCH_INDEX: BATCH_INDEX + BATCH_SIZE, :]
    cost = model.train_on_batch(X_batch, Y_batch)
    BATCH_INDEX += BATCH_SIZE
    BATCH_INDEX = 0 if BATCH_INDEX >= X_train.shape[0] else BATCH_INDEX

    if step % 500 == 0:
        cost, accuracy = model.evaluate(
            X_test, y_test, batch_size=y_test.shape[0], verbose=False)
        print('test cost: ', cost, 'test accuracy: ', accuracy)
# 有兴趣的话可以修改BATCH_SIZE和CELL_SIZE的值，试试这两个参数对训练时间和精度的影响。
