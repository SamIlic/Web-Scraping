"""
# NOTE (for Sam): Run on "QSTrader" Conda Virtual Enviroment 
    > "source activate QSTrader"
    > Run via "python coincap_ERC-20_ranker.py"

Summary of script
    1) Open Top ERC-20 file & create a DataFrame with the info
    2) Get ID's for all ERC-20 tokens using Global API
    3) Use Ticker(Specific Currency) API to get info on each ERC-20 token
    4) Create a DataFrame with all the info
    5) Write DataFrame to .xlsx file

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
from prettytable import PrettyTable
from colorama import Fore, Back, Style


### 1) Open Top ERC-20 Tokens File
file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/TokenScraper/Top ERC-20 Tokens (2018-08-05).csv"
top_ERC_df = pd.read_csv(file_path, header=0,index_col=0)

#print(df)
ERC_ticker_List = top_ERC_df.iloc[:,1]
#print(ERC_ticker_List)

# Set Currency
convert = 'USD'

# Global API URL
listings_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
url_end = '?structure=array&convert=' + convert

request = requests.get(listings_url)
results = request.json()
data = results['data']  # All Global Data

ticker_url_pairs = {}
SMALL_ticker_url_pairs = {}
iii = 0
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    if symbol in ERC_ticker_List.values:
        ticker_url_pairs[symbol] = url
        SMALL_ticker_url_pairs[symbol] = url
        iii +=1
        if iii >= 5:
            break
        

#SMALL_ticker_url_pairs = ticker_url_pairs.iloc[0:5,:]
print(SMALL_ticker_url_pairs)


# for ticker in ticker_url_pairs:
#     #print(ticker_url_pairs[ticker])
#     ticker = ticker.upper()
#     ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end
#     #print("ID: ", ticker_url_pairs[ticker])
#     request = requests.get(ticker_url)
#     results = request.json()

#     # print(json.dumps(results, sort_keys=True, indent=4))

#     ### Get Data for ticker 
#     currency = results['data'][0]
#     rank = currency['rank']
#     name = currency['name']
#     # symbol = currency['symbol']
#     # circulating_supply = int(currency['circulating_supply'])
#     # total_supply = int(currency['total_supply'])
#     # quotes = currency['quotes'][convert]
#     # market_cap = quotes['market_cap']
#     # hour_change = quotes['percent_change_1h']
#     # day_change = quotes['percent_change_24h']
#     # week_change = quotes['percent_change_7d']
#     # price = quotes['price']
#     # volume = quotes['volume_24h']
#     print(name)












