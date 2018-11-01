"""
# NOTE (for Sam): Run on "QSTrader" Conda Virtual Enviroment 
    > "source activate QSTrader"
    > Run via "python coincap_ranker.py"

Summary of script
    - This script will display top 100 rankings for the following criteria
        - 1) Top 100 sorted by rank
        - 2) Top 100 sorted by 24 hour percent change
        - 3) Top 100 sorted by 24 hour volume
    - In addition, apart from ranking coins via (1)-(2), the script 
    will also display the following for each coin
        - Token Name
        - Ticker
        - Price
        - Market Cap
        - Circulating Supply
        - Total Supply
        - % of Total Supply Circulating
        - Max Supply
        - 24h Volume
        - Change in price: 1h, 24h, 7d

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

convert = 'USD'

global_url = 'https://api.coinmarketcap.com/v2/global/' + '?convert=' + convert

request = requests.get(global_url)
results = request.json()

data = results['data']
global_cap = int(data['quotes']['USD']['total_market_cap'])
global_cap_string = '{:,}'.format(global_cap)

while True:
    print()
    print("CoinMarketCap Explorer Menu")
    print("The global market cap is $" + global_cap_string)
    print()
    print("1 - Top 100 sorted by rank")
    print("2 - Top 100 sorted by 24 hour percent change")
    print("3 - Top 100 sorted by 24 hour volume")
    print("0 - Exit")
    print()
    choice = input('What is your choice (1-3)?: ')

    ticker_url = 'https://api.coinmarketcap.com/v2/ticker/?structure=array&sort='

    if choice == '1':
        ticker_url += 'rank'
        fileName = "Top 100 - Market Cap"
    if choice == '2':
        ticker_url += 'percent_change_24h'
        fileName = "Top 100 - Daily Price Change"
    if choice == '3':
        ticker_url += 'volume_24h'
        fileName = "Top 100 - Daily Volume"
    if choice == '0':
        break

    request = requests.get(ticker_url)
    results = request.json()

    # print(json.dumps(results, sort_keys=True, indent=4))

    data = results['data']

    table = PrettyTable(['Rank', 'Asset', 'Price', 'Market Cap', ' Daily Volume', 'Circulating Supply','Total Supply','% of Total Supply Circulating','Max Supply','1h', '24h', '7d', 'Website Slug'])

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


    print()
    for currency in data:  # For each currency 
        quotes = currency['quotes'][convert]  # Quotes
        ### PrettyTable
        rank = currency['rank']
        name = currency['name']
        symbol = currency['symbol']
        price = quotes['price']
        market_cap = quotes['market_cap']
        volume = quotes['volume_24h']
        circulating_supply = currency['circulating_supply']
        total_supply = currency['total_supply']

        if circulating_supply is None:
            circulating_supply = 0
        if total_supply is None:
            percent_total_supply_circulating = "None"
        else:
            percent_total_supply_circulating = int( circulating_supply / total_supply * 100)

        max_supply = currency['max_supply']
        hour_change = quotes['percent_change_1h']
        day_change = quotes['percent_change_24h']
        week_change = quotes['percent_change_7d']
        website_slug = currency['website_slug']

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

        ### Color Code changes
        if hour_change is not None:
            if hour_change > 0:
                hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
            else:
                hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if day_change is not None:
            if day_change > 0:
                day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

        if week_change is not None:
            if week_change > 0:
                week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

        if volume is not None:
            volume_string = '{:,}'.format(volume)

        if market_cap is not None:
            market_cap_string = '{:,}'.format(market_cap)

        

        ### Create PrettyTable
        table.add_row([rank,
                       name + ' (' + symbol + ')',
                       '$' + str(price),
                       '$' + market_cap_string,
                       '$' + volume_string,
                       str(circulating_supply),
                       str(total_supply),
                       str(percent_total_supply_circulating),
                       str(max_supply),
                       str(hour_change),
                       str(day_change),
                       str(week_change),
                       str(website_slug)])

        # print(str(rank) + ': ' + name + ' (' + symbol + ')')
        # print('Market cap: \t\t$' + market_cap_string)
        # print('Price: \t\t\t$' + str(price))
        # print('24h Volume: \t\t$' + str(volume) + '%')
        # print('Hour change: \t\t' + str(hour_change) + '%')
        # print('Day change: \t\t' + str(day_change) + '%')
        # print('Week change: \t\t' + str(week_change) + '%')
        # print('Circulating supply: \t' + circulating_supply_string)
        # print('Total supply: \t\t' + total_supply_string)
        # print('Percentage circulating: ' + str(int(circulating_supply / total_supply * 100)) + '%')
        # print()

    ### Create DataFrame from Lists
    ##df = pd.DataFrame(data=temp, index=ranking)
    ranker_List = pd.DataFrame(
                    list(zip(name_List,
                             symbol_List,
                             price_List,
                             market_cap_List,
                             volume_List,
                             circulating_supply_List,
                             total_supply_List,
                             percent_total_supply_circulating_List,
                             max_supply_List,
                             hour_change_List,
                             day_change_List,
                             week_change_List,
                             website_slug_List
                             )),
                    columns=['Name',
                             'Symbol',
                             'Price',
                             'Market Cap',
                             'Daily Volume',
                             'Circulating Supply',
                             'Total Supply',
                             '% of Total Supply Circulating',
                             'Max Supply',
                             '% Change: 1h',
                             '% Change: 24h',
                             '% Change: 7d',
                             'CoinMarketCap Website Slug'],
                    index=rank_List)
    ranker_List.index.name = "Rank"  # Rename Index

        # rank = currency['rank']
        # name = currency['name']
        # symbol = currency['symbol']
        # price = quotes['price']
        # market_cap = quotes['market_cap']
        # volume = quotes['volume_24h']
        # circulating_supply = currency['circulating_supply']
        # total_supply = currency['total_supply']
        # max_supply = currency['max_supply']
        # hour_change = quotes['percent_change_1h']
        # day_change = quotes['percent_change_24h']
        # week_change = quotes['percent_change_7d']
        # website_slug = currency['website_slug']


    ### Dispaly
    print()
    print(table)
    #print(name_List)
    #print(ranker_List)
    print()

    ### Create Excel File
    #fileName = "TEST"
    file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/TokenScraper/CoinMarketCap Adv Project/" + fileName + ".xlsx"
    writer_HardDrive = pd.ExcelWriter(file_path_HardDrive)#, engine='openpyxl')
    ranker_List.to_excel(writer_HardDrive, startrow= 0 , index=True, sheet_name= 'Summary') # write to "MASTER-Ercot.xlsx" spreadsheet

    writer_HardDrive.save()
    writer_HardDrive.close()

    choice = input('Again? (y/n): ')

    if choice == 'n':
        break


