"""Here we test stuff"""


# Import libraries



# class DataPortaltp():

#     def extractall():
#         """This function extract the xml files from the Transparency Portals.
#         Usually they come in json format, but in some cases they come in xml with an embedded json.
#         After extraction they are converted into tables and storage in a Data Structurated Database for posterior analysis.
#         Normal order: Create DB -> Open Connection -> Run API -> Create DataFrame -> Save in DB"""

#         """Cleaning old DB"""
#         os.remove(local_db) if os.path.exists(local_db) else None

#         """Start connection and cursor setup"""
#         conn = sqlite3.connect(local_db)
#         type(conn)
#         cur = conn.cursor()
#         type(cur)
#         print('Database Connected!')

#         """Create table --- optional"""
#         # sql_create = 'create table licitacoes '\
#         # '(ano	decimal(4), '\
#         # 'mes	nvarchar(20), '\
#         # 'tipo_processo	nvarchar(20), '\
#         # 'unidade_gestora	nvarchar(100), '\
#         # 'modalidade	nvarchar(500), '\
#         # 'licitacao	nvarchar(30), '\
#         # 'processo	nvarchar(30), '\
#         # 'objeto	texto	nvarchar(300), '\
#         # 'abertura	datetime, '\
#         # 'homologacao	datetime, '\
#         # 'conclusao	datetime, '\
#         # 'situacao	nvarchar(20), '\
#         # 'valor_homologado	decimal(10,2))'

#         """Create dataframe"""
#         #dflicitacoes = pd.DataFrame(columns= ('ano', 'mes', 'tipo_processo', 'unidade_gestora', 'modalidade', 'licitacao', 'processo', 'objeto', 'abertura', 'homologacao', 'conclusao', 'situacao', 'valor_homologado'))
#         #cur.execute(sql_create)
#         #print('Database Created!')

#         for ano in range(initialdate.year, (finaldate.year-2)):
#             #for mes in range(1,13):
#             for mes in range(1,2):
#                 for index, row in portaltp_executivo.iterrows():
#                     for index2, it in metlist.iterrows():

#                         """Insert row names in the variables following the iteration"""
#                         link = row["Link"]
#                         mun = row["Municipio"]
#                         item = it["Metodo"]
#                         res = requests.get(str(link)+'api/transparencia.asmx/json_'+str(item)+'?ano='+str(ano)+'&mes='+str(mes))

#                         """this line bellow can be used if u want extract and work with a Json file:"""
#                         #jsonfile=(res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')

#                         """This try is necessary to don't stop the run if the API is off or another problems"""
#                         try:
#                             """Extract -> convert xlm to Json -> read JSon as a table -> convert table in Dataframe"""
#                             dflicitacoes=pd.DataFrame(pd.read_json((res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').\
#                                 replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')))
#                             print('Dataframe created!')

#                             """Create table in DB"""
#                             #tablename = ('licitacoes' + str(city))
#                             tablename = str(item)

#                             """Create a column that create key to improve the future search in DB"""
#                             dflicitacoes['Municipio'] = str(mun)
#                             #dflicitacoes['Chave'] = (str(item) + "_" + str(mun) + "_" + str(ano) + "_" + str(mes))

#                             """Check empty values and store (load) table in DB"""
#                             if dflicitacoes.empty:
#                                 print('Data ' + str(item) + ' ' + str(mun) + ' ' + str(ano) + "/" + str(mes) + ' is empty!')
#                             else:
#                                 dflicitacoes.to_sql(tablename, conn, if_exists='append')
#                                 #dflicitacoes=pd.concat([dflicitacoes, dflicitacoesaux])
#                                 print('Data ' + str(item) + ' ' + str(mun) + ' ' + str(ano) + "/" + str(mes) + ' appended')
#                         except:
#                             print('Problem in ' + str(item) + ' ' + str(mun) + ' ' + str(ano) + "/" + str(mes))

#         # print(dflicitacoesaux)
#         # print(dflicitacoes)
#         # dflicitacoes.to_sql(tablename, conn, if_exists='replace', index = False)
#         print('Data loaded to sql!')

#         #Test Code
#         #cur.execute('''  
#         #SELECT * FROM licitacoes
#         #          ''')
#         #for row in cur.fetchall():
#         #    print(row)

#         print('Database Stored!')

#         """Close connection"""
#         conn.close()

#         return print('End Database Process')

