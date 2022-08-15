"""Let's try extract all unstructured data too
Implementantion order:
1 - download pdfs
2 - organize mongoDB
3 - OCR pdfs
4 - Elastic Search
5 - semi struture the data
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

url = 'https://santamariadejetiba-es.portaltp.com.br/consultas/documentos.aspx?id=8'



def extract_contract_url(url):
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
    return df

lelele = extract_contract_url(url)

print(lelele)
