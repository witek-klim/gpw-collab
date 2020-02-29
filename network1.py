import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


from collectData import CollectCurrency


class Network1():
    def __init__(self):
        print('creating Network1')
        self.data = CollectCurrency(names = ['usd'], nyears = 4).X
        
        self.prepare_data()

    def prepare_data(self, *args, **kwargs):
        """
        prepare data by scaling to 0-1 range, or otherwise
        """
        self.X = MinMaxScaler().fit_transform(self.data.values)

    def prepare_keras(self):
        pass



if __name__== "__main__":
    network = Network1()


