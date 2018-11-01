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
import requests
import datetime
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from colorama import Fore, Back, Style



### 1) Open Top ERC-20 Tokens File
file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/TokenScraper/CoinMarketCap Dev API/CMC-ID-Map.xlsx"
# top_ERC_df = pd.read_csv(file_path, header=0,index_col=0)  # for .csv
top_ERC_df = pd.read_excel(file_path, sheetname = "Top ERC-20") # read all data from "Top ERC-20"
headers = list(top_ERC_df.columns.values) # get the headers --> ERC-20 Token, Ticker, ID, CoinMarketCap URL, Market Cap (yyyy-mm-dd) 
top_ERC_df = pd.DataFrame(top_ERC_df) # convert top_ERC_df to a DateFrame

# Get IDs
ERC_ID_List = top_ERC_df.iloc[:,2]
# print(ERC_ID_List)

# Set Currency
convert = 'USD'

### CoinMarketCap API
# EXAMPLE API KEY Call --> https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?CMC_PRO_API_KEY=a3e5008f-c6b1-471d-9b4c-c4424e8b7d1f
API_Key = '?CMC_PRO_API_KEY=3245f792-04f0-4517-86be-4c15c30edc1e' # Sam's personal API Key 
# listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/historical' + API_Key # Not Supported in Free subscription plan
listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' + API_Key   # Listings Latest
url_end = '?structure=array&convert=' + convert  # Might not be necessary anymore 

request = requests.get(listings_url)
results = request.json()
data = results['data']  # All Data
#currencyData = results['data'][0] # All Currencies

# print(json.dumps(results, sort_keys=True, indent=4))

### Initilaize List elements --> will be used to create DataFrame --> used to create .xlsx file
id_num_List = list()
name_List = list()
symbol_List = list()
website_slug_List = list()
cmc_rank_List = list()
num_markets_List = list()
circulating_supply_List = list()
total_supply_List = list()
percent_total_supply_circulating_List = list()
max_supply_List = list()
last_updated_List = list()
# ['quote']['USD']
price_List = list()
volume_24h_List = list()
market_cap_List = list()
percent_change_1h_List = list()
percent_change_24h_List = list()
percent_change_7d_List = list()

jjj = 0
#for currency in currencyData: # For each 
for currency in data: # For each 

    if currency['id'] in ERC_ID_List.values:  # ONLY FOR ERC-20 Tokens
        ### Get Data for ticker 
        id_num = currency['id']
        rank = currency['cmc_rank']
        name = currency['name']
        symbol = currency['symbol']
        website_slug = currency['slug']
        website_slug = "https://coinmarketcap.com/currencies/" + website_slug + "/"
        num_markets = currency['num_markets']
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
        last_updated = currency['last_updated']
        # Quotes
        quotes = currency['quote'][convert]
        price = round(quotes['price'],4)
        volume = round(quotes['volume_24h'])
        percent_change_1h = quotes['percent_change_1h']
        percent_change_24h = quotes['percent_change_24h']
        percent_change_7d = quotes['percent_change_7d']
        market_cap = quotes['market_cap']

        print(jjj,': ', name, " (", symbol, ")")
        jjj += 1

        ### Append List Elements
        id_num_List.append(id_num)
        cmc_rank_List.append(rank)
        name_List.append(name)
        symbol_List.append(symbol)
        website_slug_List.append(website_slug)
        num_markets_List.append(num_markets)
        circulating_supply_List.append(circulating_supply)
        total_supply_List.append(total_supply)
        max_supply_List.append(max_supply)
        last_updated_List.append(last_updated)
        price_List.append(price)
        volume_24h_List.append(volume)
        percent_change_1h_List.append(percent_change_1h)
        percent_change_24h_List.append(percent_change_24h)
        percent_change_7d_List.append(percent_change_7d)
        market_cap_List.append(market_cap)


### Create DataFrame from Lists
##df = pd.DataFrame(data=temp, index=ranking)
ranker_List = pd.DataFrame(
                list(zip(cmc_rank_List, name_List, symbol_List, price_List, market_cap_List,
                            volume_24h_List, num_markets_List, percent_total_supply_circulating_List,
                            circulating_supply_List, total_supply_List, max_supply_List,
                            percent_change_1h_List, percent_change_24h_List, percent_change_7d_List,
                            id_num_List, last_updated_List, website_slug_List)),
                columns=['Name',
                            'Ticker',
                            'Price ($)',
                            'Market Cap ($)',
                            'Daily Volume ($)',
                            'Number of Markets',
                            '% of Total Supply Circulating',
                            'Circulating Supply',
                            'Total Supply',
                            'Max Supply',
                            '% Change: 1h',
                            '% Change: 24h',
                            '% Change: 7d',
                            'ID',
                            'Last Updated',
                            'CoinMarketCap URL'],
                index=cmc_rank_List)

ranker_List.index.name = "CMC Rank"  # Rename Index

#print(name_List)
print(name_List)
print(ranker_List)

"""
### Ordering in Excel Sheet
    cmc_rank_List
    name_List
    symbol_List

    price_List
    market_cap_List
    volume_24h_List
    num_markets_List

    percent_total_supply_circulating_List
    circulating_supply_List
    total_supply_List
    max_supply_List
    
    percent_change_1h_List
    percent_change_24h_List
    percent_change_7d_List

    id_num_List
    last_updated_List
    website_slug_List
"""

# Get Time stamp for market cap
timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer

### Create Excel File
fileName = "MASTER-ERC-20" + timeStamp
file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/TokenScraper/CoinMarketCap Dev API/" + fileName + ".xlsx"
writer_HardDrive = pd.ExcelWriter(file_path_HardDrive)#, engine='openpyxl')
ranker_List.to_excel(writer_HardDrive, startrow= 0 , index=True, sheet_name= 'Summary') # write to "MASTER-Ercot.xlsx" spreadsheet

writer_HardDrive.save()
writer_HardDrive.close()













