# -*- coding: utf-8 -*-
import scrapy # needed to scrape
import xlrd   # used to easily import xlsx file 
import json
import re
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import datetime
import os
#from datetime import timedelta

# Name & Rank Pairs
Name_Rank_pairs = {}

### Global Variables
MASTER_Coin_df = pd.DataFrame()
token_name_List = list()
ticker_List = list()
exchange_count_List = list()
exchange_pair_count_List = list()
avg_pair_per_exchange_List = list()
scraped_rank_List = list()



class Markets(scrapy.Spider):
    name = 'CMC_Markets'  # Name of Script
    
    # cwd = os.getcwd()
    # print(cwd)
    # file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/DATA/COINS.xlsx"
    # MASTER_Coin_df = pd.read_excel(file_path, sheet_name = "ERC-20 (2018-08-10)") # read all data from "Top ERC-20"
    # print(list(MASTER_Coin_df.columns.values))

    # Get Time stamp for market cap
    timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer

    # set file path
    fileName =  "MASTER-1000" + timeStamp + ".xlsx"
    file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/DATA/MASTER-1000" + timeStamp + ".xlsx"
    # file_path = file_path.encode('unicode_escape')
    # print(file_path)

    # create df
    MASTER_Coin_df = pd.read_excel(file_path, sheet_name = "API Data") # read all data from "Top ERC-20"
    headers = list(MASTER_Coin_df.columns.values) # get the headers --> ERC-20 Token, Ticker, ID, CoinMarketCap URL, Market Cap (yyyy-mm-dd) 
    print(list(MASTER_Coin_df.columns.values))



#     # URLs
#     URLs = MASTER_Coin_df['CoinMarketCap URL']
#     temp_urls = URLs.values.tolist()
#     temp_urls = [url + "#markets" for url in temp_urls]

#     # Set Name & Rank Pairs
#     coin_names = MASTER_Coin_df['Name']
#     ranks = MASTER_Coin_df[headers[0]] # "CMC Rank (yyyy-mm-dd)"
#     iii = 1
#     for coin_name in coin_names: # Rank 1-1000
#         Name_Rank_pairs[coin_name] = iii # set pairs
#         iii += 1
    

#     print("``````````````````````````````````````````````````````````````````````````````")
#     # start_urls = ['https://coinmarketcap.com/currencies/tron/#markets']  # TEST
#     start_urls = temp_urls
#     print("``````````````````````````````````````````````````````````````````````````````")

# ################################################################################################
# ################################################################################################

#     """
#     Scrape Daily Ercot data and Append to "MASTER-Ercot" file
#     """
#     def parse(self, response):
#         self.logger.info('A response has arrived from %s', response.url)
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
#         ### Ticker
#         tickerTemp = response.css("body > div.container.main-section > div > div.col-lg-10.padding-top-1x > div.details-panel.flex-container.bottom-margin-2x > div.details-panel-item--header.flex-container > h1 > span::text").extract()[0]

#         ### Get total num exchage-pairs
#         temp_rank_List = list()
#         temp_source_List = list()
#         count = 1
#         while(True):
#             iii = str(count)
#             try:
#                 tempRank   = response.css("#markets-table > tbody > tr:nth-child(" + iii + ") > td:nth-child(1)::text").extract()[0]
#                 tempSource = response.css("#markets-table > tbody > tr:nth-child(" + iii + ") > td:nth-child(2) > a::text").extract()[0]
#                 token_name = response.css("body > div.container.main-section > div > div.col-lg-10.padding-top-1x > div.details-panel.flex-container.bottom-margin-2x > div.details-panel-item--header.flex-container > h1::text").extract()[1].strip()
#                 # No Error Thrown
#                 temp_rank_List.append(tempRank)
#                 temp_source_List.append(tempSource)
#                 count += 1
#             except IndexError:
#                 break
        
        
#         exchange_count = len(list(set(temp_source_List)))  # Remove duplicate exchanges
#         exchange_pair_count = len(temp_rank_List)  # Total number of trading piars
#         avg_pair_per_exchange = round(exchange_pair_count/exchange_count,1)  # Average number of trading pairs per exchange

#         #print("Rank List: ", temp_rank_List)
#         print('Token Name: ', token_name)
#         print("Length Temp Rank List: ", len(temp_rank_List))
#         print("Exchange Count: ", exchange_count)
#         print("Pair Count: ", exchange_pair_count)
#         print("Average Pairs per Exchange: ", avg_pair_per_exchange)

#         ### Append
#         # Name
#         token_name_List.append(token_name)
#         # Ticker
#         ticker_List.append(tickerTemp[1:len(tickerTemp) - 1])
#         # Exchange Count
#         exchange_count_List.append(exchange_count)
#         # Pair Count
#         exchange_pair_count_List.append(exchange_pair_count)
#         # Average Pairs per Exchange
#         avg_pair_per_exchange_List.append(avg_pair_per_exchange)
#         # Rank
#         try:
#             scraped_rank_List.append(Name_Rank_pairs[token_name])
#         except:
#             scraped_rank_List.append(1000000)

            

        
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


#     """
#     Run after the Scrapy is done scraping/crawling
#     """
#     def closed( self, reason ):
#         # Get Time stamp for market cap
#         timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer
        
#         ### Sanity Check
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         print('Name: ', len(token_name_List))
#         print('Ticker: ',len(ticker_List))
#         print('Exchange Count: ', len(exchange_count_List))
#         print('Exchange Pair Count: ', len(exchange_pair_count_List))
#         print('Average Pair: ', len(avg_pair_per_exchange_List))
#         print('Rank: ', len(scraped_rank_List))
#         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
#         ### Create DataFrame
#         Markets_df = pd.DataFrame(list(zip(token_name_List,
#                                            ticker_List,
#                                            exchange_count_List, 
#                                            exchange_pair_count_List,
#                                            avg_pair_per_exchange_List)),
#                                    columns=['Name',
#                                             'Ticker',
#                                             'Number of Exchanges',
#                                             'Number of Exchange Trading Pairs',
#                                             'Avg Number of Trading Pairs per Exchange'],
#                                     index=scraped_rank_List)
#         Markets_df.index.name = "CMC Rank" + timeStamp  # Rename Index

#         # Sort DataFrame by Index
#         # Markets_df.sort_values(by=['Name'])
#         Markets_df=Markets_df.sort_index() # Sort by CMC Rank (index)

#         ### Create new Tab in "MASTER ERC-20.xlsx"
#         # set file path
#         fileName =  "MASTER-1000" + timeStamp + ".xlsx"
#         # file_path_HardDrive = "/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/DATA/" + fileName
#         # file_path_HardDrive = file_path_HardDrive.encode('unicode_escape')
#         #file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/DATA/MASTER-1000 (2018-08-14).xlsx"

#         # Open file
#         file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/DATA/MASTER-1000 (2018-08-14).xlsx"
#         writer_HardDrive = pd.ExcelWriter(file_path_HardDrive, engine='openpyxl')

#         # Write to new sheet in existing workbook
#         book_HardDrive = load_workbook(file_path_HardDrive)
#         writer_HardDrive.book = book_HardDrive

#         # Write Sheet
#         Markets_df.to_excel(writer_HardDrive, startrow= 0 , index=True, sheet_name= 'Markets' + timeStamp)

#         writer_HardDrive.save()
#         writer_HardDrive.close()






