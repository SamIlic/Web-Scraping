"""
# NOTE (for Sam): Run on "QSTrader" Conda Virtual Enviroment 


Summary of script
    - Creates an .xlsx file for the ID map of all coins on CoinMarketCAp

# NOTE: Code must be run on a Virtual Environment in order to import "prettytable" (as least this was the case for me)
"""

import xlrd 
import re
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from datetime import timedelta

import json
import requests
from datetime import datetime
from colorama import Fore, Back, Style



# EXAMPLE API KEY Call --> https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?CMC_PRO_API_KEY=a3e5008f-c6b1-471d-9b4c-c4424e8b7d1f
API_Key = '?CMC_PRO_API_KEY=3245f792-04f0-4517-86be-4c15c30edc1e' 
listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map' + API_Key  # CoinMarketCap ID map

request = requests.get(listings_url)
results = request.json()
data = results['data']  # All Global Data

# print(json.dumps(results, sort_keys=True, indent=4))

### Initilaize List elements --> will be used to create DataFrame --> used to create .xlsx file
name_List = list()
symbol_List = list()
id_num_List = list()
first_historical_data_List = list()
is_active_List = list()
slug_List = list()

for currency in data:  # For each currency/token in JSON from API call

    name = currency['name']
    symbol = currency['symbol']
    id_num = currency['id']
    first_historical_data = currency['first_historical_data']
    is_active = currency['is_active']
    slug = currency['slug']
    slug = "https://coinmarketcap.com/currencies/" + slug + "/"

    ### Append List Elements
    name_List.append(name)
    symbol_List.append(symbol)
    id_num_List.append(id_num)
    first_historical_data_List.append(first_historical_data)
    is_active_List.append(is_active)
    slug_List.append(slug)

### Create DataFrame from Lists
##df = pd.DataFrame(data=temp, index=ranking)
ranker_List = pd.DataFrame(
                list(zip(name_List,
                        symbol_List,
                        first_historical_data_List,
                        is_active_List,
                        slug_List,
                        )),
                columns=['Name',
                        'Symbol',
                        'First Historical Data Date',
                        'Is Active',
                        'Website'],
                index=id_num_List)
ranker_List.index.name = "ID"  # Rename Index
    

### Create Excel File
fileName = "CMC-ID-Map"
file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/TokenScraper/CoinMarketCap Dev API/" + fileName + ".xlsx"
writer_HardDrive = pd.ExcelWriter(file_path_HardDrive)#, engine='openpyxl')
ranker_List.to_excel(writer_HardDrive, startrow=0, index=True, sheet_name= 'ID Map') # write to "MASTER-Ercot.xlsx" spreadsheet

writer_HardDrive.save()
writer_HardDrive.close()
















