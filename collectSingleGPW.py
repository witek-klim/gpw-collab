import requests
from datetime import datetime
            
class CollectSingleGPW():
    def __init__(self, date=None):
        """ date in format: 'dd-mm'yyyy'  """
        
        self.date = date if date is not None else datetime.today().strftime('%d-%m-%Y')
        print(self.date)
        self.url = r'https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument=&date={}&show_x=Poka%C5%BC+wyniki'.format(self.date)
        print(self.url)
        self.picklename = './{}.pkl'.format(self.date)
        self.runDataCollection()
        
    def collectData(self):    
        myfile = requests.get(self.url)
        data = myfile.content.split(b'section')[7].split(b'<td class="left">')
        df = pd.DataFrame({'name': [], 'opening': [], 'maximum':[], 'minimum':[],'closing':[], 'chamge_percent':[]})
        for i in range(1,len(data)):
            temp = data[i].replace(b' ', b'').replace(b'\t', b'').replace(b'&nbsp;',b'').replace(b'</td>\n', b'').replace(b',', b'.').split(b'<tdclass="text-right">')
            name, opening, maximum, minimum, closing, change_percent = temp[0].decode("utf-8") , float(temp[2]), float(temp[3]), float(temp[4]), float(temp[5]), float(temp[6])
            print(name, opening, maximum, minimum, closing, change_percent)
            dftemp = pd.DataFrame([[name, opening, maximum, minimum, closing, change_percent]],
                                    columns = ['name', 'opening', 'maximum', 'minimum','closing', 'chamge_percent'])
            df = df.append(dftemp)
        self.df = df
        df.to_pickle(self.picklename)
        
    def runDataCollection(self):
        try:
            self.df = pd.read_pickle(self.picklename)
            print('read data from pickle for date: {}'.format(self.date))
        except FileNotFoundError:
            self.collectData()
            print('collected data from web for date: {}'.format(self.date))
    
       
        
