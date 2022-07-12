"""Read the website creator and define new tables for each different API.
This process is necessary because every API may have a diferent approach to extract your data
the extract function will create diferent databases for each API, and the future integration will be done in SQL
Know APIs: portaltp, agape, tectrilha"""

import pandas as pd

"""Configs"""

local_apilist = 'data/lista_apis.csv'
apilist = pd.read_csv(local_apilist)

"""Portaltp - Executivo"""

portaltp_executivo=apilist.query('API_Executivo == "portaltp"')
del portaltp_executivo["Link_Legislativo"]
del portaltp_executivo["API_Legislativo"]
del portaltp_executivo["Unnamed: 5"]
del portaltp_executivo["API_Executivo"]
portaltp_executivo = portaltp_executivo.rename(columns={'Link_Executivo':'Link'})

#print(portaltp_executivo)

"""Portaltp - Legislativo"""

portaltp_legislativo=apilist.query('API_Legislativo == "portaltp"')
del portaltp_legislativo["Link_Executivo"]
del portaltp_legislativo["API_Legislativo"]
del portaltp_legislativo["Unnamed: 5"]
del portaltp_legislativo["API_Executivo"]
portaltp_legislativo = portaltp_legislativo.rename(columns={'Link_Legislativo':'Link'})

#print(portaltp_legislativo)

print('API_organization Loaded!')

