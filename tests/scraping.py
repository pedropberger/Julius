"""Testing Web Scraping and Crawling"""


import requests
from bs4 import BeautifulSoup

URL = 'http://www.nasdaq.com/symbol/amd/historical'
print('url stored')
page = requests.get(URL).text
print('request feito')
soup = BeautifulSoup(page, 'lxml')
print('pacote aplicado')
tableDiv = soup.find_all('div', id="historicalContainer")
print("tabela dividida")
tableRows = tableDiv[0].findAll('tr')
print('tabela criada')

for tableRow in tableRows[2:]:
    row = tuple(tableRow.getText().split())
    print ('"%s",%s,%s,%s,%s,"%s"' % row)


