##### All starts here

##testing commit

##Test2



import _thread
import threading
import logging
import csv
import requests
import json
from unicodedata import normalize
from bs4 import BeautifulSoup


# def getDados(cidade, linkAPI, poder):
#     try:
#         print(linkAPI + '/api/pessoal/servidor?exercicio=2020&mes=01')
#         resultado = requests.get(linkAPI + '/api/pessoal/servidor?exercicio=2020&mes=01')
#
#         j = json.loads(resultado.text)
#
#         # print(resultado)
#         # soup = BeautifulSoup(resultado.content)
#         # print(soup.find("a", href=True)['href'])
#         # csv = requests.get(soup.find("a", href=True)['href'])
#         # print(csv.content)

resultado = request.get('https://santamariadejetiba-es.portaltp.com.br/api/transparencia.asmx/json_licitacoes?ano=2017&mes=1')
j = json.loads(resultado.text)