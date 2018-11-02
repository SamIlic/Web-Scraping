"""
Summary of script
    - Use Pro CMC API to scrape current info for TOP TOKENS 
    - Create a DataFrame
    - Write to .xlsx file
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

### CoinMarketCap API
API_Key = NotRealKey # Sam's personal API Key 
# listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/historical' + API_Key # Not Supported in Free subscription plan
#listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?' + API_Key   # Listings Latest
listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=1000&sort=market_cap&convert=USD&' + API_Key   # Listings Latest

### Handle Data
request = requests.get(listings_url)
results = request.json()
data = results['data']  # All Data

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
date_added_List = list()
# ['quote']['USD']
price_List = list()
volume_24h_List = list()
market_cap_List = list()
percent_change_1h_List = list()
percent_change_24h_List = list()
percent_change_7d_List = list()

for currency in data: # Extract data for each currency in the JSON file 
    ### Get Data for ticker 
    id_num = currency['id']
    rank = currency['cmc_rank']
    name = currency['name']
    symbol = currency['symbol']
    website_slug = currency['slug']
    website_slug = "https://coinmarketcap.com/currencies/" + website_slug + "/"
    num_markets = currency['num_market_pairs']
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
    date_added = currency['date_added']
    # Quotes
    quotes = currency['quote']['USD']
    price = round(quotes['price'],4)
    volume = round(quotes['volume_24h'])
    percent_change_1h = quotes['percent_change_1h']
    percent_change_24h = quotes['percent_change_24h']
    percent_change_7d = quotes['percent_change_7d']
    market_cap = quotes['market_cap']

    ### Append List Elements
    id_num_List.append(id_num)
    cmc_rank_List.append(rank)
    name_List.append(name.strip())
    symbol_List.append(symbol)
    num_markets_List.append(num_markets)
    percent_total_supply_circulating_List.append(percent_total_supply_circulating)
    circulating_supply_List.append(circulating_supply)
    total_supply_List.append(total_supply)
    max_supply_List.append(max_supply)
    last_updated_List.append(last_updated)
    date_added_List.append(date_added)
    price_List.append(price)
    volume_24h_List.append(volume)
    percent_change_1h_List.append(percent_change_1h)
    percent_change_24h_List.append(percent_change_24h)
    percent_change_7d_List.append(percent_change_7d)
    market_cap_List.append(market_cap)
    website_slug_List.append(website_slug)

# ### Sanity Check
# print('RANK LIST', len(cmc_rank_List))
# print('NAME LIST', len(name_List))
# print('SYMBOL LIST', len(symbol_List))
# print('PRICE LIST', len(price_List))
# print('MARKET CAP LIST', len(market_cap_List))
# print('VOLUME LIST', len(volume_24h_List))
# print('NUM MARKETS LIST', len(num_markets_List))
# print('% Total LIST', len(percent_total_supply_circulating_List))
# print('CIRC SUPLPPLY LIST', len(circulating_supply_List))
# print('TOTAL SUPPLY LIST', len(total_supply_List))
# print('MAX SUPPLY LIST', len(max_supply_List))
# print('PRICE CHANGE LIST', len(percent_change_24h_List))
# print('LAST UPDATED LIST', len(last_updated_List))
# print('WEBSITE LIST', len(website_slug_List))
# print()

# Get Time stamp for market cap
timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer

### Create DataFrame from Lists
Ranked_List_df = pd.DataFrame(list(zip(name_List,
                                    symbol_List,
                                    price_List,
                                    market_cap_List,
                                    volume_24h_List,
                                    num_markets_List,
                                    percent_total_supply_circulating_List,
                                    circulating_supply_List,
                                    total_supply_List,
                                    max_supply_List,
                                    percent_change_24h_List,
                                    last_updated_List,
                                    date_added_List,
                                    website_slug_List)),
                            columns=['Name',
                                    'Ticker',
                                    'Price ($)',
                                    'Market Cap ($)',
                                    'Daily Volume ($)',
                                    'Number of Market Pairs',
                                    'Pct. of Total Supply Circulating (%)',
                                    'Circulating Supply',
                                    'Total Supply',
                                    'Max Supply',
                                    'Price Change 24h (%)',
                                    'Last Updated',
                                    'Date Added',
                                    'CoinMarketCap URL'],
                            index=cmc_rank_List)
Ranked_List_df.index.name = "CMC Rank" + timeStamp # Rename Index

# print(Ranked_List_df)

################################################################
################################################################

### Create Excel File ###
fileName = "MASTER-1000" + timeStamp
file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/Dashboard/Data/" + fileName + ".xlsx"
writer_HardDrive = pd.ExcelWriter(file_path_HardDrive, engine='openpyxl')

# # Write to new sheet in existing workbook
# book_HardDrive = load_workbook(file_path_HardDrive)
# writer_HardDrive.book = book_HardDrive

# Write Sheet
Ranked_List_df.to_excel(writer_HardDrive, startrow= 0 , index=True, sheet_name= 'API Data') # write to "MASTER-Ercot.xlsx" spreadsheet

# Save & Close 
writer_HardDrive.save()
writer_HardDrive.close()













