"""
functions in this script are used to download data from web for currency and stock history of selected names

"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
print(sys.argv, len(sys.argv))
import numpy as np
import time


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
        plt.figure(dpi = dpi)
        plt.plot(self.X)
        plt.grid('major', linewidth = 0.1)
        plt.legend()
        plt.xlabel('time')
        plt.show()

    def find_change(self, period = 1):
        """
        think about better name for this function
        it is supposed to calculate relative change e.g. day to day instead of quoting the absolute value
        """
        self.X = self.X.diff(period)
        # df = self.X
        # temp = pd.DataFrame()
        # for name in self.names:
        #     temp[name] = np.append(0, self.X[name].values[1:]) - np.append(0, self.X[name].values[:-1])
        # self.X = temp

class CollectCurrency(CollectData):
    """
    data format from stooq: [Data,Otwarcie,Najwyzszy,Najnizszy,Zamkniecie]
    """

    def __init__(self, names, quantity = 'Zamkniecie', mastercurr = 'pln', date0 = None, daten = None,
                                 nyears = 10, datapath = '/home/witek/Documents/gpw-collab/data'):
        super().__init__(names, date0 = date0, daten = daten, nyears = nyears)


        if names == []:
            self.names = ['ars','aud','brl','btc','cad','chf','clp','cny','czk','dkk','egp','gbp',
            'hkd','huf','ils','inr','isk','jpy','krw','mxn','myr','nad','nok','nzd','php',
            'ron','rub','sek','sgd','thb','try','twd','xag','xau','xpd','xpt','zar']
        else:
            self.names = names
        print(datapath)
        self.datapath = datapath
        self.mastercurr = mastercurr
        self.quantity = quantity
        self.X = self.collect_currency()
        
    def collect_currency(self):
        data = []
        for name in self.names:
            try:
                filename = f'{self.datapath}/currency_{name}_{self.date0_str}_{self.daten_str}'
                temp = pd.read_csv(filename)[['Data', name]]
                #temp = temp
            except FileNotFoundError:
                temp = pd.read_csv(f'https://stooq.pl/q/d/l/?s={name}{self.mastercurr}&d1={self.date0_str}&d2={self.daten_str}&i=d',
                                    infer_datetime_format = True)[['Data', self.quantity]].rename(columns={self.quantity: name})
                temp[name].to_csv(filename)
            # for j, day in enumerate(temp['Data']):
            #     temp['Data'][j] = datetime.datetime.strptime(day, '%Y-%m-%d')
            temp = temp.set_index('Data')
            print(temp)
            data.append(temp)
        return pd.concat(data, axis = 1).reindex(data[0].index)#.reset_index()




#curr = CollectCurrency()
#print(curr[0:2]['Zamkniecie'])
class CollecStock(CollectData):
    def __init__(self, names, quantity = 'Zamkniecie', date0 = None, daten = None,
                        nyears = 10, datapath = '/home/witek/Documents/gpw-collab/data'):
        super().__init__(names, date0 = date0, daten = daten, nyears = nyears)
        self.datapath = datapath
        self.quantity = quantity

    def collect_stock(self):
        names = ['cdr', 'dnp']
        columns = ['Data','Zamkniecie']
        date0 = datetime.datetime(2015,1,1)
        data = [None]*len(names)
        i=0
        for name in names:
            temp = pd.read_csv(f'https://stooq.pl/q/d/l/?s={name}&i=d')[columns]
            j=0
            for date in temp['Data']:
                temp['Data'][j] = datetime.datetime.strptime(date, '%Y-%m-%d')
                j += 1
            temp = temp.loc[data[i]['Data'] > date0]
            print(f'is null {temp.isnull().sum()}')
            print(f'number of days {len(temp.index)}')
            data[i] = temp
            i+=1


if __name__ == "__main__":
    curr = CollectCurrency(names = ['chf', 'usd','eur', 'jpy', 'aud', 'gbp'], nyears = 5)
    curr.find_change()



