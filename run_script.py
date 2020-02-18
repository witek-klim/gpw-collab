import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
print(sys.argv, len(sys.argv))


company = sys.argv[1]







# waluty
def CollectCurrency():
    names = ['ars','aud','brl','btc','cad','chf','clp','cny','czk','dkk','egp','gbp','hkd','huf','ils','inr','isk','jpy','krw','mxn','myr','nad','nok','nzd','php','ron','rub','sek','sgd','thb','try','twd','xag','xau','xpd','xpt','zar']
    i = 0
    data = [None] * len(names)
    for name in names:
        data[i] = pd.read_csv(f'https://stooq.pl/q/l/?s={name}pln&f=sd2t2ohlc&h&e=csv')
        i+=1
    return data

curr = CollectCurrency()
print(curr[0:2]['Zamkniecie'])

def CollectStock():
    names = ['cdr', 'dnp', company]
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
