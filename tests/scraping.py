"""Testing Web Scraping and Crawling"""


import requests
from bs4 import BeautifulSoup

URL = 'http://www.nasdaq.com/symbol/amd/historical'
page = requests.get(URL).text
soup = BeautifulSoup(page, 'lxml')
tableDiv = soup.find_all('div', id="historicalContainer")
tableRows = tableDiv[0].findAll('tr')

for tableRow in tableRows[2:]:
    row = tuple(tableRow.getText().split())
    print ('"%s",%s,%s,%s,%s,"%s"' % row)


