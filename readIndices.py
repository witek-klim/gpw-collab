# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 08:19:23 2020

@author: WK5521
"""
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime


class readIndices():
    def __init__(self, url):
        """  date   """
        self.url = url

        self.date = datetime.today().strftime('%Y-%m-%d')
        #self.date = date


        self.unpickle()

    def readURL(self):
        def simple_get(url = self.url):
            """
            Attempts to get the content at `url` by making an HTTP GET request.
            If the content-type of response is some kind of HTML/XML, return the
            text content, otherwise return None.
            """
            try:
                with closing(get(url, stream=True)) as resp:
                    if is_good_response(resp):
                        return resp.content
                    else:
                        return None

            except RequestException as e:
                log_error('Error during requests to {0} : {1}'.format(url, str(e)))
                return None


        def is_good_response(resp):
            """
            Returns True if the response seems to be HTML, False otherwise.
            """
            content_type = resp.headers['Content-Type'].lower()
            return (resp.status_code == 200 
                    and content_type is not None 
                    and content_type.find('html') > -1)


        def log_error(e):
            """
            It is always a good idea to log errors. 
            This function just prints them, but you can
            make it do anything.
            """
            print(e)

        a = simple_get()
        my_json = a.decode('utf8')
        data = my_json.split('<a title=')
        df = pd.DataFrame( {'nazwa': [], 'kurs': [], 'zmiana':[], 'transakcje':[], 'obrot':[]})

        index = 0
        for el in data[1:]:
            temp = el.split('"')
            name = temp[1]
            i = 0
            while i<len(temp):
                if temp[i][:3] == 'col':
                    break
                else:
                    i+=1
            kurs = float(temp[i+1].replace('>','<').split('<')[1].replace(',','.').replace('&nbsp;',''))
            zmiana = float(temp[i+3].replace('>','<').split('<')[1].replace(',','.').replace('&nbsp;',''))
            zmianap = float(temp[i+5].replace('>','<').split('<')[1].replace(',','.').replace('&nbsp;','').replace('%',''))
            transakcje = float(temp[i+7].replace('>','<').split('<')[1].replace(',','.').replace('&nbsp;',''))
            obrot = float(temp[i+9].replace('>','<').split('<')[1].replace(',','.').replace('&nbsp;',''))
            dftemp = pd.DataFrame({'nazwa': name, 'kurs': kurs, 'zmiana':zmiana, 'transakcje': transakcje, 'obrot': obrot}, index = [index])
            
            dftemp2 = pd.DataFrame([ [name,  kurs, zmiana,zmianap, transakcje, obrot]], columns = ['nazwa', 'kurs', 'zmiana', 'zmianap', 'transakcje', 'obrot'])
            df = df.append(dftemp2)
            index += 1
        name = './{}.pkl'.format(self.date)
        df.to_pickle(name)

    def unpickle(self):
        try:
            name = './{}.pkl'.format(self.date)
            self.unpickled_df = pd.read_pickle(name)
        except FileNotFoundError:
            self.readURL()
            self.unpickle()

    def printSummary(self):
        print(self.unpickled_df)  
        #for i in range (len(self.unpickled_df)):
        
            #print('{}\t{}\t{}'.format(self.unpickled_df['nazwa'][i], self.unpickled_df['kurs'][i], self.unpickled_df['zmianap'][i]))



url = 'https://www.bankier.pl/gielda/notowania/akcje'
case = Analysis(url)
case.printSummary()