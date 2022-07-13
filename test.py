"""Here we test stuff"""

import pandas as pd
import requests

""" local_apilist = 'data/lista_apis.csv'

apilist = pd.read_csv(local_apilist)
print(apilist)

portaltp_executivo=apilist.query('API_Executivo == "portaltp"')
del portaltp_executivo["Link_Legislativo"]
del portaltp_executivo["API_Legislativo"]
del portaltp_executivo["Unnamed: 5"]
del portaltp_executivo["API_Executivo"]
portaltp_executivo.rename(columns={'Link_Executivo':'Link'}, inplace=True)

print(portaltp_executivo) """


itens = 'data/APImethods.txt'
with open(itens) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

for i in lines:
    print(lines)



""" for index, row in apilist.iterrows():
    s = row["Municipio"]
    c = row['API_Executivo']
    i = row["Link_Executivo"]
    if c == 'portaltp':
        print(i)
        print(str(s) + ' ' + str(i))
        res=requests.get(i + 'api/transparencia.asmx/json_licitacoes?ano=2020&mes=1')
        print(res) """


#    print(res)




    # dflicitacoes=pd.DataFrame(pd.read_json((res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').\
    #     replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')))
    # print('Dataframe created!')

    #             #Create table in DB
    # tablename = ('licitacoes' + 'SMJ')

    #             #Check empty values and store (load) table in DB
    # if dflicitacoes.empty:
    #     print('Data ' + 'licitacoes' + i + ' is empty!')














"""Think about use iloc over iterows, which is more efficient?

for i in range(len(df)):
    print(df.iloc[i, 0], df.iloc[i, 2])"""