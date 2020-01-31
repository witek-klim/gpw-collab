import os
import matplotlib
from collectSingleGPW import CollectSingleGPW
from datetime import datetime

class collectData():
    """ collect data for specified time regime """
    def __init__(self, fromDate, toDate = None):
        """ date in format 'dd-mm-yyyy'  """
        self.fromDate = fromDate
        self.toDate = toDate if toDate!= None else datetime.today().strftime('%d-%m-%Y')
        
    def findRequiredDays(self):
        self.days = [] # list of days for which data is to be collected in standard dd-mm-yyyy format
        

        
