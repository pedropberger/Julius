"""Let's try extract all unstructured data too
Implementantion order:

0 - Scrap tables and contract's url
1 - download pdfs
2 - organize mongoDB
3 - OCR pdfs
4 - Elastic Search
5 - Semi struture the data
6 - Full Portal Scraping/Crawling (not only the first page)

---------------------------------------
Example sites
https://colatina-es.portaltp.com.br/consultas/documentos.aspx?id=8
https://santamariadejetiba-es.portaltp.com.br/consultas/documentos.aspx?id=8
http://santateresa-es.portaltp.com.br/consultas/documentos.aspx?id=8

"""

import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

#Loading configs
initialdate = []
finaldate = []
portaltp_executivo=[]
metlist = []
local_apilist = []
local_db = []
url = []
df2 = []
exec(open("scripts/API_organization.py").read())
exec(open("config.py").read())

url_end_aux = 'consultas/documentos.aspx?id=8'


class DataPortaltp_Unstructured():

    def url_creation():
        for index, row in portaltp_executivo.iterrows():
            link = row["Link"]
            mun = row["Municipio"]
            url=(str(link) + str(url_end_aux))

            """Fase1: Parsing the website and use BeautifulSoup package to replicate the table with the URLs to download the contract files
                Fase2: Parsing the website and use Pandas to extract the table with contract information
                Param:
                url: url of the contract website page
            """
            #Fase1            
            res = requests.get(url)
            html_page = res.text
            soup = BeautifulSoup(html_page, 'html.parser')
            soup.prettify()
            urllist=[]
            for link in soup.find_all('a',{"class": "dxbs-hyperlink"}):
                urllist.append(link.get('href'))
            del urllist[-2:]
            #Fase2
            df_list = pd.read_html(res.content)
            df = df_list[-1]
            df = df.iloc[1: , :]
            df = df[:-1]
            df['Arquivo'] = np.array(urllist)
            print(df)
            #df2=pd.concat([df2, df])
            #print('concated')

DataPortaltp_Unstructured.url_creation()


# siteslist = DataPortaltp_Unstructured.url_creation(portaltp_executivo)
# print(siteslist)

# table = contract_df_extract(siteslists, url)
# print(table)





"""======================================================================================================================="""


# class DataPortaltp_Unstructured():
#     """Extract data unstructured from Portals and catalog them in a non-relational database
#     This process need web scrapping and crawling to find the urls and download the data    
#     """

#     def url_creation(siteslist):
#         for index, row in siteslist.iterrows():
#             link = row["Link"]
#             mun = row["Municipio"]
#             url.append(str(link) + str(url_end_aux))
#         return url

#     def extract_contract_url(url_site):
#         """Fase1: Parsing the website and use BeautifulSoup package to replicate the table with the URLs to download the contract files
#             Fase2: Parsing the website and use Pandas to extract the table with contract information
#             Param:
#             url: url of the contract website page
#         """
#         #Fase1
#         res = requests.get(url_site)
#         html_page = res.text
#         soup = BeautifulSoup(html_page, 'html.parser')
#         soup.prettify()
#         urllist=[]
#         for link in soup.find_all('a',{"class": "dxbs-hyperlink"}):
#             urllist.append(link.get('href'))
#         del urllist[-2:]
#         #Fase2
#         df_list = pd.read_html(res.content)
#         df = df_list[-1]
#         df = df.iloc[1: , :]
#         df = df[:-1]
#         df['Arquivo'] = np.array(urllist)
#         return df


# def contract_df_extract(siteslist, url):
#     for index in url:
#         url_site = index
#         print(url_site + ' inserido com sucesso')
#         df = DataPortaltp_Unstructured.url_creation(url_site)
#         print(df)
#         df_contract = pd.concat([df_contract, df])
#         return(df_contract)



# siteslist = DataPortaltp_Unstructured.url_creation(portaltp_executivo)
# print(siteslist)

# table = contract_df_extract(siteslists, url)
# print(table)

