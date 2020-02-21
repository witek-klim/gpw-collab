"""
functions in this script are used to download data from web for currency and stock history of selected names

"""




import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
print(sys.argv, len(sys.argv))

import time
import sys

from sklearn.preprocessing import MinMaxScaler


class CollectData():
    """
    names: pick either names of currencies or stock companies to collect data for
    date0: string in format "yyyy-mm-dd"

    attributes are in pandas.DataFrame format:
        - X: inputs
        - y: outputs
    
    """
    def __init__(self, names, date0 = None, daten = None, outputs = 1, nyears = 10):
        print('collecting data')
        self.names = names
        self.X = None

        self.daten = datetime.date.today()
        self.daten_str = self.daten.strftime("%Y%m%d")

        if date0 is None:
            self.date0 = datetime.date(self.daten.year - nyears, self.daten.month, self.daten.day)
        else:
            self.date0 = datetime.datetime.strptime(date0, '%Y-%m-%d')
        self.date0_str = self.date0.strftime("%Y%m%d")

    def check_data(self):
        nullsX = self.X.isnull().sum()
        print(f'null elements in X:\n{nullsX}')
        

    def plot_data(self, dpi = 100, skip = 10):
        """
        skip: use to plot only every skip value from data
        """
        from pandas.plotting import register_matplotlib_converters
        register_matplotlib_converters()
        i = 1
        plt.figure(dpi = dpi)
        for name in self.names:
            plt.plot(self.X['Data'][::skip], self.X.values[:,i][::skip], label = name)
            i+=1
        plt.grid('major', linewidth = 0.1)
        plt.legend()
        plt.xlabel('time')
        plt.ylabel('PLN')
        plt.show()



class CollectCurrency(CollectData):
    """
    data format from stooq: Data,Otwarcie,Najwyzszy,Najnizszy,Zamkniecie
    """

    def __init__(self, names, quantity = 'Zamkniecie', mastercurr = 'pln', date0 = None, daten = None, nyears = 10):
        super().__init__(names, date0 = date0, daten = daten, nyears = nyears)
        if names == []:
            self.names = ['ars','aud','brl','btc','cad','chf','clp','cny','czk','dkk','egp','gbp',
            'hkd','huf','ils','inr','isk','jpy','krw','mxn','myr','nad','nok','nzd','php',
            'ron','rub','sek','sgd','thb','try','twd','xag','xau','xpd','xpt','zar']
        else:
            self.names = names

        self.mastercurr = mastercurr
        self.quantity = quantity
        self.X = self.collect_currency()
        
    def collect_currency(self):
        i = 0
        data = [None] * len(self.names)
        for name in self.names:
            data[i] = pd.read_csv(f'https://stooq.pl/q/d/l/?s={name}{self.mastercurr}&d1={self.date0_str}&d2={self.daten_str}&i=d')[['Data', self.quantity]].rename(columns={self.quantity: name})
            j=0
            for d in data[i]['Data']:
                data[i]['Data'][j] = datetime.datetime.strptime(d, '%Y-%m-%d')
                j+=1
            data[i] = data[i].set_index('Data')
            i+=1
        data = pd.concat(data, axis = 1).reindex(data[0].index).reset_index()
        return data



curr = CollectCurrency(names = ['chf', 'usd','eur', 'jpy', 'aud', 'gbp'], nyears = 3)
#curr.check_data()
curr.plot_data(dpi = 120)


from scipy.stats import pearsonr
X = curr.X

import seaborn as sns
plt.figure()
cor = X.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()




