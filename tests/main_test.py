import requests
import pandas as pd


"""Configs"""

local_apilist = 'data/lista_apis.csv'
local_metlist = 'data/APImethods.csv'
apilist = pd.read_csv(local_apilist)
metlist = pd.read_csv(local_metlist)

"""Separa as prefeituras que tem o modelo de Portal da Transparência da E&L (portaltp)"""

portaltp_executivo=apilist.query('API_Executivo == "portaltp"')
del portaltp_executivo["Link_Legislativo"]
del portaltp_executivo["API_Legislativo"]
del portaltp_executivo["Unnamed: 5"]
del portaltp_executivo["API_Executivo"]
portaltp_executivo = portaltp_executivo.rename(columns={'Link_Executivo':'Link'})

print(portaltp_executivo)

"""Separa as câmaras que tem o modelo de Portal da Transparência da E&L (portaltp)"""

portaltp_legislativo=apilist.query('API_Legislativo == "portaltp"')
del portaltp_legislativo["Link_Executivo"]
del portaltp_legislativo["API_Legislativo"]
del portaltp_legislativo["Unnamed: 5"]
del portaltp_legislativo["API_Executivo"]
portaltp_legislativo = portaltp_legislativo.rename(columns={'Link_Legislativo':'Link'})

print(portaltp_legislativo)

print('API_organization Loaded!')


def loop_municipio_prefeitura_tp():
    """
    Loop em todos municípios
    
    """
    pass

for index, row in portaltp_executivo.iterrows():
    print(row["Municipio"])

res = requests.get("http://santamariadejetiba-es.portaltp.com.br/api/transparencia.asmx/json_licitacoes?ano=2017&mes=1")
#print(res)

try:

    dflicitacoes=pd.DataFrame(pd.read_json((res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').\
        replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')))
    print('Dataframe created!')
    print(dflicitacoes)

except:
    print('Problems happens')