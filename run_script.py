from collectSingleGPW import CollectSingleGPW
from collectData import CollectData


a = CollectData(2020, company = 'DINOPL')

#a = CollectSingleGPW('02-01-2020', storePath = r'C:/Users/wk5521/Documents/gpwdata/' )
print(a.values)

