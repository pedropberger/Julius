#import json
from distutils.command.config import config
from typing_extensions import Self
from numpy import extract
import py
import requests
import pandas as pd
import os
import sqlite3
#import datetime
#import time
#import json
#import requests
#import xmltodict
#import pandas as pd
#from concurrent.futures import thread
#from distutils.command.config import config
#import py
from threading import *
import time
from datetime import date
from dateutil.relativedelta import relativedelta


"""
TASKS:
1 - Change the DB from SQLite to MongoDB
2 - Refactor the code to use more functions and less repetition
3 - Refactor loops to funcions
4 - Try

"""

start = time.time()

#Loading configs
initialdate = []
finaldate = []
portaltp_executivo=[]
metlist = []
local_apilist = []
local_db = []
exec(open("scripts/API_organization.py").read())
exec(open("config.py").read())

"""Here are the config files, directories or parameters that can change in all places"""

from datetime import date
from dateutil.relativedelta import relativedelta

"""Date of begin and end of extracted data"""

initialdate = date(2022,7,1)
finaldate = date.today() + relativedelta(months=-2)
print('Data inicial de busca: ' + str(initialdate) + ' Ano-Mês-Dia')
print('Data final de busca: ' + str(finaldate))

"""Path configs"""

local_apilist = 'data/lista_apis.csv'
local_db = 'D:\TempData\Julius.db'


"""Database Configs"""

mysql = {
    "host": "localhost",
    "user": "root",
    "passwd": "my secret password",
    "db": "write-math",
}




"""Cleaning old DB"""
os.remove(local_db) if os.path.exists(local_db) else None

"""Start connection and cursor setup"""
conn = sqlite3.connect(local_db)
type(conn)
cur = conn.cursor()
type(cur)
print('Database Connected!')

"""Create table --- optional"""
# sql_create = 'create table licitacoes '\
# '(ano	decimal(4), '\
# 'mes	nvarchar(20), '\
# 'tipo_processo	nvarchar(20), '\
# 'unidade_gestora	nvarchar(100), '\
# 'modalidade	nvarchar(500), '\
# 'licitacao	nvarchar(30), '\
# 'processo	nvarchar(30), '\
# 'objeto	texto	nvarchar(300), '\
# 'abertura	datetime, '\
# 'homologacao	datetime, '\
# 'conclusao	datetime, '\
# 'situacao	nvarchar(20), '\
# 'valor_homologado	decimal(10,2))'

"""Create dataframe"""
#dflicitacoes = pd.DataFrame(columns= ('ano', 'mes', 'tipo_processo', 'unidade_gestora', 'modalidade', 'licitacao', 'processo', 'objeto', 'abertura', 'homologacao', 'conclusao', 'situacao', 'valor_homologado'))
#cur.execute(sql_create)
#print('Database Created!')

for ano in range(initialdate.year, (finaldate.year)):
    #for mes in range(1,13):
    for mes in range(1,13):
        for index, row in portaltp_executivo.iterrows():
            for index2, it in metlist.iterrows():

                """Insert row names in the variables following the iteration"""
                link = row["Link"]
                mun = row["Municipio"]
                item = it["Metodo"]
                res = requests.get(str(link)+'api/transparencia.asmx/json_'+str(item)+'?ano='+str(ano)+'&mes='+str(mes))

                """this line bellow can be used if u want extract and work with a Json file:"""
                #jsonfile=(res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')

                """This try is necessary to don't stop the run if the API is off or another problems"""
                try:
                    """Extract -> convert xlm to Json -> read JSon as a table -> convert table in Dataframe"""
                    dflicitacoes=pd.DataFrame(pd.read_json((res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').\
                        replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')))
                    print('Dataframe created!')
                    

                    """Create table in DB"""
                    #tablename = ('licitacoes' + str(city))
                    tablename = str(item)

                    """Create a column that create key to improve the future search in DB"""
                    dflicitacoes['Municipio'] = str(mun)
                    #dflicitacoes['Chave'] = (str(item) + "_" + str(mun) + "_" + str(ano) + "_" + str(mes))

                    """Check empty values and store (load) table in DB"""
                    if dflicitacoes.empty:
                        print('Data ' + str(item) + ' ' + str(mun) + ' ' + str(ano) + "/" + str(mes) + ' is empty!')
                    else:
                        dflicitacoes.to_sql(tablename, conn, if_exists='append')
                        #dflicitacoes=pd.concat([dflicitacoes, dflicitacoesaux])
                        #print('Data ' + str(item) + ' ' + str(mun) + ' ' + str(ano) + "/" + str(mes) + ' appended')
                        print('Data {item} {mun} {ano}/{mes} appended'.format(item=str(item), mun=str(mun), ano=str(ano), mes=str(mes)))
                except:
                    print('Problem in ' + str(item) + ' ' + str(mun) + ' ' + str(ano) + "/" + str(mes))

# print(dflicitacoesaux)
# print(dflicitacoes)
# dflicitacoes.to_sql(tablename, conn, if_exists='replace', index = False)
print('Data loaded to sql!')

#Test Code
#cur.execute('''  
#SELECT * FROM licitacoes
#          ''')
#for row in cur.fetchall():
#    print(row)

print('Database Stored!')

"""Close connection"""
conn.close()

print('End Database Process')