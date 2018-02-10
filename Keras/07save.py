import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

# create some data
X = np.linspace(-1, 1, 200)
np.random.shuffle(X)    # randomize the data
Y = 0.5 * X + 2 + np.random.normal(0, 0.05, (200, ))
X_train, Y_train = X[:160], Y[:160]     # first 160 data points
X_test, Y_test = X[160:], Y[160:]       # last 40 data points
model = Sequential()
model.add(Dense(output_dim=1, input_dim=1))
model.compile(loss='mse', optimizer='sgd')
for step in range(301):
    cost = model.train_on_batch(X_train, Y_train)

# save
"""
训练完模型之后，可以打印一下预测的结果，接下来就保存模型。
保存的时候只需要一行代码 model.save，再给它加一个名字就可以用 h5 的格式保存起来。
这里注意，需要已经安装了 HDF5 这个模块。
保存完模型之后，删掉它，后面可以来比较是否成功的保存。
"""
print('test before save: ', model.predict(X_test[0:2]))
model.save('my_model.h5')   # HDF5 file, you have to pip3 install h5py if don't have it
del model  # deletes the existing model

# load
# 导入保存好的模型，再执行一遍预测，与之前预测的结果比较，可以发现结果是一样的。
model = load_model('my_model.h5')
print('test after load: ', model.predict(X_test[0:2]))

"""
# save and load weights
另外还有其他保存模型并调用的方式，第一种是只保存权重而不保存模型的结构
model.save_weights('my_model_weights.h5')
model.load_weights('my_model_weights.h5')
"""
"""
# save and load fresh network without trained weights
第二种是用 model.to_json 保存完结构之后，然后再去加载这个json_string。
from keras.models import model_from_json
json_string = model.to_json()
model = model_from_json(json_string)
"""

