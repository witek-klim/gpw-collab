import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
print(sys.argv, len(sys.argv))




# waluty
def CollectCurrency():
    names = ['ars','aud','brl','btc','cad','chf','clp','cny','czk','dkk','egp','gbp','hkd','huf','ils','inr','isk','jpy','krw','mxn','myr','nad','nok','nzd','php','ron','rub','sek','sgd','thb','try','twd','xag','xau','xpd','xpt','zar']
    i = 0
    data = [None] * len(names)
    for name in names:
        data[i] = pd.read_csv(f'https://stooq.pl/q/l/?s={name}pln&f=sd2t2ohlc&h&e=csv')
        i+=1
    return data

#curr = CollectCurrency()
#print(curr[0]['Zamkniecie'])

def CollectStock():
    names = ['cdr', 'dnp']
    columns = ['Data','Zamkniecie']
    date0 = datetime.datetime(2015,1,1)
    data = [None]*len(names)
    i=0
    for name in names:
        data[i] = pd.read_csv(f'https://stooq.pl/q/d/l/?s={name}&i=d')[columns]
        j=0
        for date in data[i]['Data']:
            data[i]['Data'][j] = datetime.datetime.strptime(date, '%Y-%m-%d')
            j += 1
        data[i] = data[i].loc[data[i]['Data'] > date0]
        print(f'is null {data[i].isnull().sum()}')
        print(f'number of days {len(data[i].index)}')
        i+=1

    plt.figure()
    for i in range(len(names)):
        plt.plot(data[i]['Data'], data[i]['Zamkniecie'], label = names[i])
    plt.legend()
    plt.grid('major', linewidth = .1)
    plt.show()




f =  lambda x: (x-0.5)**2
x = np.linspace(0,1,4)
y = f(x)

#plt.plot(x,y)
#plt.show()

from tensorflow import keras

model = keras.Sequential()
# activations are: 'sigmoid', 'relu', 'selu', 'softmax', 'sofplus', 'softsign', 'tanh', 'sigmoid', 'hard_sigmoid'
# 'linear', 'exponential', 'elu'
activation = 'softmax'
model.add(keras.layers.Dense(20, input_shape=(1,), activation = activation))
model.add(keras.layers.Dense(20, activation = activation))
model.add(keras.layers.Dense(20, activation = activation))
model.add(keras.layers.Dense(1))
optimizer = keras.optimizers.RMSprop(0.001)

model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])

model.summary()
EPOCHS = 400
# history has following keys: 'loss', 'val_loss', 'mean_squared_error', 'val_mean_squared_error'
history = model.fit( x,y,
  epochs=EPOCHS, validation_split = 0.2, verbose=0 )


xs = np.linspace(0,1,100)
ys = model.predict(xs)
plt.plot(x,y,'ko',mfc = 'None', label = 'training data')
plt.plot(xs, ys,label = 'prediction')
plt.legend()
plt.grid('major')
plt.show()

print(type(history))
print(history)

plt.plot(history.history['loss'], label='MAE (testing data)')
plt.plot(history.history['val_loss'], label='MAE (validation data)')
plt.title('MAE for Chennai Reservoir Levels')
plt.ylabel('MAE value')
plt.xlabel('No. epoch')
plt.legend(loc="upper left")
plt.show()