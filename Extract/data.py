#import json
from typing_extensions import Self
from numpy import extract
import py
import requests
import pandas as pd
import os
import sqlite3

class Data():

    def extract():
        """This function extract the xml files from the Transparency Portals.
        Usually they come in json format, but in some cases they come in xml with an embedded json.
        After extraction they are converted into tables and storage in a Data Structurated Database for posterior analysis."""

        res = requests.get('https://santamariadejetiba-es.portaltp.com.br/api/transparencia.asmx/json_licitacoes?ano=2022&mes=1')

        """this line bellow can be used if u want extract and work with a Json file."""
        #jsonfile=(res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')

        #Extract -> convert xlm to Json -> read JSon as a table -> convert table in Dataframe
        dflicitacoes=pd.DataFrame(pd.read_json((res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')))
        
        print('Dataframe created!')
        
        os.remove("C:\TempData\licitacoes.db") if os.path.exists("C:\TempData\licitacoes.db") else None

        conn = sqlite3.connect('C:\TempData\licitacoes.db')

        type(conn)

        cur = conn.cursor()

        type(cur)

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

        dflicitacoes.to_sql('licitacoes', conn, if_exists='replace', index = False)

        print('Data loaded to sql!')

        cur.execute('''  
        SELECT * FROM licitacoes
                  ''')

        for row in cur.fetchall():
            print(row)

        print('Database Stored')

        conn.close()
        return print('End Database Process')