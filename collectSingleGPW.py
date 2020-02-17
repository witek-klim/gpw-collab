import requests
from datetime import datetime
import pandas as pd
            
class CollectSingleGPW():
    def __init__(self, date=None, save2pickle = False, verbose = True, storePath = None):
        """ date in format: 'dd-mm'yyyy'  """

        self.date = date if date is not None else datetime.today().strftime('%d-%m-%Y')
        self.storePath = storePath
        self.save2pickle = save2pickle
        self.url = r'https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument=&date={}&show_x=Poka%C5%BC+wyniki'.format(self.date)
        self.picklename = self.storePath+ '/{}.pkl'.format(self.date)
        self.verbose = verbose
        self.runDataCollection()

        
    def runDataCollection(self):
        if self.verbose:
            print('-------------------------------------')
        try:
            self.data = pd.read_pickle(self.picklename)
            if self.verbose:
                print('read data from pickle for date: {}'.format(self.date))
        except FileNotFoundError:
            self.collectDataFromWeb()
            if self.verbose:
                print('collected data from web for date: {}'.format(self.date))

        if self.checkData() and self.save2pickle:
            if self.verbose:
                print('saving to pickle')
            self.save2Pickle()

    def collectDataFromWeb(self):
        """  collect data from web  """    
        myfile = requests.get(self.url)
        data = myfile.content.split(b'section')[7].split(b'<td class="left">')
        df = pd.DataFrame({'name': [], 'opening': [], 'maximum':[], 'minimum':[],'closing':[], 'change_percent':[]})
        for i in range(1,len(data)):
            temp = data[i].replace(b' ', b'').replace(b'\t', b'').replace(b'&nbsp;',b'').replace(b'</td>\n', b'').replace(b',', b'.').split(b'<tdclass="text-right">')
            name, opening, maximum, minimum, closing, change_percent = temp[0].decode("utf-8") , float(temp[2]), float(temp[3]), float(temp[4]), float(temp[5]), float(temp[6])
            dftemp = pd.DataFrame([[name, opening, maximum, minimum, closing, change_percent]],
                                    columns = ['name', 'opening', 'maximum', 'minimum','closing', 'change_percent'])
            df = df.append(dftemp)
        self.data = df.set_index('name')
    
    def checkData(self):
        """ check data for correctness """
        if self.data.shape[0] == 0:
            if self.verbose:
                print('data incorrect\n')
            return False
        else:
            if self.verbose:
                print('data correct!\n')
            return True

    def save2Pickle(self):
        self.data.to_pickle(self.picklename)


