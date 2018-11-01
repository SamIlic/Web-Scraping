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

import re
import xlrd 
import json
import time
import requests
import datetime
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from prettytable import PrettyTable
from colorama import Fore, Back, Style


# ### 1) Open Top ERC-20 Tokens File CSV
# file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/TokenScraper/Top ERC-20 Tokens (2018-08-05).csv"
# top_ERC_df = pd.read_csv(file_path, header=0,index_col=0)

### 1) Open Top-ERC-20 Tokens File
file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/TokenScraper/Top-ERC-20.xlsx"
top_ERC_df = pd.read_excel(file_path, sheetname = "Summary") # read all data from "Top ERC-20"
headers = list(top_ERC_df.columns.values) # get the headers --> ERC-20 Token, Ticker, ID, CoinMarketCap URL, Market Cap (yyyy-mm-dd) 
top_ERC_df = pd.DataFrame(top_ERC_df) # convert top_ERC_df to a DateFrame



#print(df)
ERC_ticker_List = top_ERC_df.iloc[:,1] # 1 bc the first column are indices
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
        # iii +=1
        # if iii >= 5:
        #     break
#SMALL_ticker_url_pairs = ticker_url_pairs.iloc[0:5,:]
#print("SMALL_ticker_url_pairs: ", SMALL_ticker_url_pairs)

print()

### Initilaize List elements --> will be used to create DataFrame --> used to create .xlsx file
quotesList = list()  # Quotes
rank_List = list()
name_List = list()
symbol_List = list()
price_List = list()
market_cap_List = list()
volume_List = list()
circulating_supply_List = list()
total_supply_List = list()
percent_total_supply_circulating_List = list()
max_supply_List = list()
hour_change_List = list()
day_change_List = list()
week_change_List = list()
website_slug_List = list()

jjj = 0
for ticker in ticker_url_pairs:
    ### TIME DELAY --> Can only Call API 10 times per minute
    time.sleep(7)  # 10 Sec Time Delay

    #print(ticker_url_pairs[ticker])
    ticker = ticker.upper()
    ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end
    #print("ID: ", ticker_url_pairs[ticker])
    request = requests.get(ticker_url)
    results = request.json()

    # print(json.dumps(results, sort_keys=True, indent=4))
    currency = results['data'][0]
    quotes = currency['quotes'][convert]  # Quotes
    ### Get Data for ticker 
    rank = currency['rank']
    name = currency['name']
    symbol = currency['symbol']
    price = round(quotes['price'],4)
    market_cap = quotes['market_cap']
    volume = round(quotes['volume_24h'])
    circulating_supply = currency['circulating_supply']
    total_supply = currency['total_supply']

    if circulating_supply is None:
        circulating_supply = 0    
    if total_supply is None:
        total_supply = 0
        percent_total_supply_circulating = "None"
    else:
        # percent_total_supply_circulating = int(round(circulating_supply/total_supply*100))
        percent_total_supply_circulating = round(circulating_supply/total_supply*100)

    max_supply = currency['max_supply']
    hour_change = quotes['percent_change_1h']
    day_change = quotes['percent_change_24h']
    week_change = quotes['percent_change_7d']
    website_slug = currency['website_slug']
    website_slug = "https://coinmarketcap.com/currencies/" + website_slug + "/"
    
    print(jjj,': ', name, " (", symbol, ")")
    jjj += 1

    ### Append List Elements
    rank_List.append(rank)
    name_List.append(name)
    symbol_List.append(symbol)
    price_List.append(price)
    market_cap_List.append(market_cap)
    volume_List.append(volume)
    circulating_supply_List.append(circulating_supply)
    total_supply_List.append(total_supply)
    percent_total_supply_circulating_List.append(percent_total_supply_circulating)
    max_supply_List.append(max_supply)
    hour_change_List.append(hour_change)
    day_change_List.append(day_change)
    week_change_List.append(week_change)
    website_slug_List.append(website_slug)

print()

# Get Time stamp for market cap
timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer

### Create DataFrame from Lists
##df = pd.DataFrame(data=temp, index=ranking)
ranker_List = pd.DataFrame(
                list(zip(name_List,
                            symbol_List,
                            price_List,
                            market_cap_List,
                            volume_List,
                            percent_total_supply_circulating_List,
                            circulating_supply_List,
                            total_supply_List,
                            max_supply_List,
                            hour_change_List,
                            day_change_List,
                            week_change_List,
                            website_slug_List
                            )),
                columns=['Name',
                            'Ticker',
                            'Price ($)',
                            'Market Cap ($)',
                            'Daily Volume ($)',
                            '% of Total Supply Circulating',
                            'Circulating Supply',
                            'Total Supply',
                            'Max Supply',
                            '% Change: 1h',
                            '% Change: 24h',
                            '% Change: 7d',
                            'CoinMarketCap Website Slug'],
                index=rank_List)
ranker_List.index.name = "Rank " + timeStamp  # Rename Index


### Create Excel File
fileName = "MASTER ERC-20" #+ timeStamp
file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/TokenScraper/CoinMarketCap Adv Project/" + fileName + ".xlsx"
writer_HardDrive = pd.ExcelWriter(file_path_HardDrive)#, engine='openpyxl')
ranker_List.to_excel(writer_HardDrive, startrow= 0 , index=True, sheet_name= 'Summary') # write to "MASTER-Ercot.xlsx" spreadsheet

writer_HardDrive.save()
writer_HardDrive.close()









