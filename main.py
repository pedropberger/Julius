##### All starts here

#import json
#import requests
#import xmltodict
#import pandas as pd
from distutils.command.config import config
from Extract.data import Data

# import sys
# for path in sys.path:
#     print(path)

def main():
    print("Partiu!")
    Data.extract()

if __name__ == "__main__":
    main()