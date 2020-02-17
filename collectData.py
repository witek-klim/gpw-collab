import os
import matplotlib
from collectSingleGPW import CollectSingleGPW
from datetime import datetime
import numpy as np

class CollectData():
    """ collect data for specified time regime """
    def __init__(self, fromYear, company, toDate = None):
        """ date in format 'dd-mm-yyyy'  """
        self.fromYear = fromYear
        self.toDate = toDate if toDate!= None else datetime.today().strftime('%d-%m-%Y')
        path = os.getcwd()
        self.storepath = path + '/gpwdata/'
        #self.storepath = r'C:/Users/wk5521/Documents/gpwdata/'
        self.days = []
        self.findRequiredDays()
        self.collect()
        
    def findRequiredDays(self):        
         # list of days for which data is to be collected in standard dd-mm-yyyy format
         # used to collect data and save to pickle
         
        def compareDays(d1, d2):
            if int(d1[-4:]) > int(d2[-4:]):
                return True
            elif int(d1[-4:]) < int(d2[-4:]):
                return False
            elif int(d1[3:5]) > int(d2[3:5]):
                return True
            elif int(d1[3:5]) < int(d2[3:5]):
                return False
            elif int(d1[:2]) > int(d2[:2]):
                return True
            else:
                return False

        day = range(1,32)
        month = range(1,13)
        year = range(self.fromYear, 2021)

        for y in year:
            for m in month:
                for d in day:
                    self.days.append('{:02d}-{:02d}-{:04d}'.format(d, m, y))
                    if compareDays(self.days[-1], self.toDate):
                        break 

    def collect(self, company = None, indices = 'all'):
        """ indices is a list containing required data to be returned, e.g.: ['name', 'closing']  """

        #columns = CollectSingleGPW(date, save2pickle = True, storePath = self.storepath, verbose = True).columns
        values = np.zeros(len(self.days))
        #def runcollect():
        i = 0
        for date in self.days:
            print(f'collecting for {date}')
            singleGPW = CollectSingleGPW(date, save2pickle = True, storePath = self.storepath, verbose = True)
            if singleGPW.checkData():
                values[i] = singleGPW.data.loc[company, 'closing']

        self.values = values
        
        

