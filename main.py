"""Welcome to Julius!

This is a simple code created to extract data from all City Transparency Portals of the state of Espírito Santo, Brazil.
Every portal has your own API, but they have similar patterns (depends on the company that create them).
We catalog them in 4 diferent patterns to extract data in a efficient way.

You have 2 ways to execute this code. Using threads or not.
If you choose use threading you can select how API methods (data clusters) u want extract.
A full extract consumes 4gb of you hard disk."""

"""All starts here"""

#import json
#import requests
#import xmltodict
#import pandas as pd
from distutils.command.config import config
import py
from scripts.data import Data

"""Select your way
1 - Full Extract
2 - Multithreading"""

way = 2

def main():
    
    if way == 1:
        print("Partiu!")
        Data.extract()
    else:
        print("Bora fast")
        Data.dbclean()
        conn = Data.dbstart()
        Data.licitacoes(conn)
        Data.dbclose(conn)

if __name__ == "__main__":
    main()