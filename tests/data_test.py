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

#Loading configs
initialdate = []
finaldate = []
portaltp_executivo=[]
metlist = []
local_apilist = []
local_db = []
exec(open("scripts/API_organization.py").read())
exec(open("config.py").read())

"""######## Testing change the code in a class ########"""


class DataDataDB():        

    def dbclean():
        """Cleaning old DB"""

        os.remove("C:\TempData\Julius.db") if os.path.exists("C:\TempData\Julius.db") else None
        return print('Database Cleaned!')

    def dbstart():
        """Start connection and cursor setup"""

        conn = sqlite3.connect('C:\TempData\Julius.db')
        type(conn)
        cur = conn.cursor()
        type(cur)
        print('Conection to Database Created')
        return conn

    def dbclose(conn):
        """Close connection"""

        conn.close()

        return print('Database Closed')

    def extract(conn, methodapi):
        """Extract only one data cluster"""

        item = str(methodapi)
        for ano in range(initialdate.year, (finaldate.year-2)):
            #for mes in range(1,13):
            for mes in range(1,2):
                for index, row in portaltp_executivo.iterrows():
                    link = row["Link"]
                    mun = row["Municipio"]

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
                        dflicitacoes['Chave'] = (str(item) + "_" + str(mun) + "_" + str(ano) + "_" + str(mes))

                        """Check empty values and store (load) table in DB"""

                        if dflicitacoes.empty:
                            print('Data ' + str(item) + ' ' + str(mun) + ' ' + str(ano) + "/" + str(mes) + ' is empty!')
                        else:
                            dflicitacoes.to_sql(tablename, conn, if_exists='append')
                            #dflicitacoes=pd.concat([dflicitacoes, dflicitacoesaux])
                            print('Data ' + str(item) + ' ' + str(mun) + ' ' + str(ano) + "/" + str(mes) + ' appended')
                    except:
                        print('Problem in ' + str(item) + ' ' + str(mun) + ' ' + str(ano) + "/" + str(mes))
        return print('All ' + str(item) + ' extracted!')

    """######################################################################
         Here to the end are clones of the function above for testing
    #########################################################################"""

"""
way = 2

def main():
    
    if way == 1:
        print("Partiu!")
        DataPortaltp.extractall()
    else:
        print("Bora fast!")
        DataPortaltp.dbclean()
        conn = DataPortaltp.dbstart()
        DataPortaltp.licitacoes(conn)
        DataPortaltp.dbclose(conn)

if __name__ == "__main__":
    main()"""