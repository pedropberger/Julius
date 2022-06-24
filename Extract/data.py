import json
import requests
import xmltodict
import pandas as pd

class Data():
    def extract():
        """This function extract the xml files from the Transparency Portals.
        Usually they come in json format, but in some cases they come in xml with an embedded json.
        After extraction they are converted into tables for later storage or analysis."""

        res = requests.get('https://santamariadejetiba-es.portaltp.com.br/api/transparencia.asmx/json_licitacoes?ano=2022&mes=1')
        #this line bellow can be used if u want extract and work with a Json file.
        #jsonfile=(res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>')
        x=pd.read_json((res.text).replace('<?xml version="1.0" encoding="utf-8"?>','').replace('<string xmlns="http://tempuri.org/">', '').removesuffix('</string>'))
        return print(x)