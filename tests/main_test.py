import requests
import pandas as pd

res = requests.get("http://santamariadejetiba-es.portaltp.com.br/api/transparencia.asmx/json_licitacoes?ano=2017&mes=1")
print(res)

try:

    dflicitacoes=pd.DataFrame(pd.read_json((res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').\
        replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')))
    print('Dataframe created!')

except:
    print('Problems happens')