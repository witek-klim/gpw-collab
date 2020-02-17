from collectSingleGPW import CollectSingleGPW
from collectData import CollectData
import os
path = os.getcwd()
storepath = path + '/gpwdata/'

cumul = CollectData(2020, company = 'CDPROJEKT')

single = CollectSingleGPW('02-01-2020', save2pickle = True, storePath = storepath)
print(single.data.loc[['DINOPL', 'CDPROJEKT']])
print(single.data.loc['CDPROJEKT', 'opening'])


#print(cumul)


