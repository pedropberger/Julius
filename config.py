"""Here are the config files, directories or parameters that can change in all places"""

from datetime import date
from dateutil.relativedelta import relativedelta

#Date of begin and end of extracted data


initialdate = str(date(2019,1,1))
finaldate = str(date.today() + relativedelta(months=-2))
print('Data inicial de busca: ' + initialdate + ' Ano-Mês-Dia')
print('Data final de busca: ' + finaldate + '\n Você pode alterar a data final no arquivo config.py' + '\n por padrão a busca ocorre com dois meses de defasagem da data atual')