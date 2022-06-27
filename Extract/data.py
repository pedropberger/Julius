#import json
from distutils.command.config import config
from typing_extensions import Self
from numpy import extract
import py
import requests
import pandas as pd
import os
import sqlite3
import datetime

#executando configurações
exec(open("config.py").read())

class Data():

    def extract():
        """This function extract the xml files from the Transparency Portals.
        Usually they come in json format, but in some cases they come in xml with an embedded json.
        After extraction they are converted into tables and storage in a Data Structurated Database for posterior analysis.
        Normal order: Create DB -> Open Connection -> Run API -> Create DataFrame -> Save in DB"""

        #Cleaning old DB
        os.remove("C:\TempData\Julius.db") if os.path.exists("C:\TempData\Julius.db") else None
        #os.remove("C:\TempData\licitacoes.db") if os.path.exists("C:\TempData\licitacoes.db") else None

        #Start connection and cursor setup
        conn = sqlite3.connect('C:\TempData\Julius.db')
        type(conn)
        cur = conn.cursor()
        type(cur)
        print('Database Connected!')

        #Create table --- In the future we need to transfer that for a DB application
        sql_create = 'create table licitacoes '\
        '(ano	decimal(4), '\
        'mes	nvarchar(20), '\
        'tipo_processo	nvarchar(20), '\
        'unidade_gestora	nvarchar(100), '\
        'modalidade	nvarchar(500), '\
        'licitacao	nvarchar(30), '\
        'processo	nvarchar(30), '\
        'objeto	texto	nvarchar(300), '\
        'abertura	datetime, '\
        'homologacao	datetime, '\
        'conclusao	datetime, '\
        'situacao	nvarchar(20), '\
        'valor_homologado	decimal(10,2))'

        cur.execute(sql_create)

        print('Database Created!')

        for ano in range(initialdate.year, finaldate.year):
            res = requests.get('https://santamariadejetiba-es.portaltp.com.br/api/transparencia.asmx/json_licitacoes?ano='+str(ano)+'&mes=1')

            """this line bellow can be used if u want extract and work with a Json file:
            jsonfile=(res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')"""

            #Extract -> convert xlm to Json -> read JSon as a table -> convert table in Dataframe
            dflicitacoes=pd.DataFrame(pd.read_json((res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').\
                replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')))
            print('Dataframe created!')
            
            #Update (load) table to DB
            tablename = ('licitacoes' + str(ano))

            dflicitacoes.to_sql(tablename, conn, if_exists='replace', index = False)
            print('Data loaded to sql!')

        #Test Code
        #cur.execute('''  
        #SELECT * FROM licitacoes
        #          ''')
        #for row in cur.fetchall():
        #    print(row)

        print('Database Stored!')

        #Close connection
        conn.close()

        return print('End Database Process')