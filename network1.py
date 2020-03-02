import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import copy

from collectData import CollectCurrency


class Network1():
    def __init__(self):
        print('creating Network1')
        self.data = CollectCurrency(names = ['usd'], nyears = 4).X
        self.look_back = 1
        self.train_test = True
        self.prepare_data()

    def prepare_data(self, *args, **kwargs):
        """
        prepare data by scaling to 0-1 range, or otherwise
        hence prepare data to appropriate format: here LSTM 
        """
        self.X = MinMaxScaler().fit_transform(self.data.values)
        
        #    [samples, time steps, features]
        self.Y = copy.deepcopy(self.X[self.look_back:])
        self.X = self.X[:-self.look_back]

        self.X = self.X.reshape([self.X.shape[0], 1, self.X.shape[1]])

        
        if self.train_test:
            # assume 4 to 1 split
            self.X_train = self.X[:int(self.X.shape[0] * .8)]
            self.X_test = self.X[int(self.X.shape[0] * .2):]


            self.Y_train = self.Y[:int(self.Y.shape[0] * .8)]
            self.Y_test = self.Y[int(self.Y.shape[0] * .2):]

    def prepare_keras(self):
        """"""

        model = keras.Sequential()
        model.add(keras.layers.LSTM(6, input_shape = (1,self.look_back)))
        model.add(keras.layers.Dense(1))
        model.compile(loss = 'mean_squared_error', optimizer = 'adam')
        model.fit(self.X_train,self.Y_train, epochs = 10, batch_size=1, verbose=2)

        self.model = model

        trainPredict = model.predict(self.X_train)
        testPredict = model.predict(self.X_test)

        plt.plot(trainPredict, 'k-', label = 'train')
        plt.plot(testPredict, 'k--', label = 'test')
        plt.plot(self.Y)
        plt.show()

if __name__== "__main__":
    network = Network1()
    network.prepare_keras()


