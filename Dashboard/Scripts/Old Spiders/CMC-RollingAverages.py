# -*- coding: utf-8 -*-
import scrapy # needed to scrape
import xlrd   # used to easily import xlsx file 
import json
import re
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import datetime
#from datetime import timedelta

# Name & Rank Pairs
Name_Rank_pairs = {}

### Global Variables
MASTER_ERC_df = pd.DataFrame()
token_name_List = list()
ticker_List = list()
rolling_avg_volume_monthly_List = list()
rolling_avg_volume_weekly_List = list()
scraped_rank_List = list()



class Rolling(scrapy.Spider):
    name = 'CMC-RollingAverages'  # Name of Script
    
    # Get Time stamp for market cap
    timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer
    
    fileName =  "MASTER-1000" + timeStamp + ".xlsx"
    # file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/Data/COINS.xlsx"
    file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/Data/" + fileName
    MASTER_Coin_df = pd.read_excel(file_path, sheet_name = "API Data") # read all data from "Top ERC-20"
    headers = list(MASTER_Coin_df.columns.values) # get the headers --> ERC-20 Token, Ticker, ID, CoinMarketCap URL, Market Cap (yyyy-mm-dd) 
   
    # URLs
    URLs = MASTER_Coin_df['CoinMarketCap URL']
    temp_urls = URLs.values.tolist()
    temp_urls = [url + "historical-data/" for url in temp_urls]

    # Set Name & Rank Pairs
    coin_names = MASTER_Coin_df['Name']
    ranks = MASTER_Coin_df[headers[0]] # "CMC Rank (yyyy-mm-dd)"
    iii = 1
    for coin_name in coin_names: # Rank 1-1000
        Name_Rank_pairs[coin_name] = iii # set pairs
        iii += 1


    print("``````````````````````````````````````````````````````````````````````````````")
    # start_urls = ['https://coinmarketcap.com/currencies/tron/historical-data/']  # TEST
    start_urls = temp_urls
    print("``````````````````````````````````````````````````````````````````````````````")

################################################################################################
################################################################################################

    """
    Scrape Daily Ercot data and Append to "MASTER-Ercot" file
    """
    def parse(self, response):
        self.logger.info('A response has arrived from %s', response.url)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        # Get Ticker
        tickerTemp = response.css("body > div.container.main-section > div > div.col-lg-10.padding-top-1x > div.details-panel.flex-container.bottom-margin-2x > div.details-panel-item--header.flex-container > h1 > span::text").extract()[0]
        ticker_List.append(tickerTemp[1:len(tickerTemp) - 1])  # Append
        
        # Create temp lists
        temp_volume_monthly_List = list()
        temp_volume_weekly_List = list()


        # Get Monthly Volume & Market Cap lists
        try: 
            # Monthly Values
            for iii in list(range(1,31)):
                iii = str(iii)
                temp_volume_monthly_List.append(response.css("#historical-data > div > div.table-responsive > table > tbody > tr:nth-child(" + iii + ") > td:nth-child(6)::text").extract()[0])
                # temp_volume_weekly_List.append(response.css("#historical-data > div > div.table-responsive > table > tbody > tr:nth-child(" + iii + ") > td:nth-child(7)::text").extract()[0])
            # Weekly Values
            temp_volume_weekly_List = temp_volume_monthly_List[0:7]
            print(temp_volume_weekly_List)
        except: # Less than 1 Month of data
            print("##########################")
            print("EXCEPTION THROWN: LESS than 1 MONTH of data")
            print("##########################")
            try:
                temp_volume_weekly_List = temp_volume_monthly_List[0:7]
            except: # Less than 1 Week of data
                print("##########################")
                print("EXCEPTION THROWN: LESS than 1 WEEK of data")
                print("##########################")
                temp_volume_weekly_List = temp_volume_monthly_List[0:len(temp_volume_monthly_List)]


        # Covert list of Strings to Ints
        temp_volume_monthly_List = [int(i.replace(',','')) for i in temp_volume_monthly_List]
        temp_volume_weekly_List = [int(i.replace(',',''))  for i in temp_volume_weekly_List]

        ### Append
        # Name
        token_name = response.css("body > div.container.main-section > div > div.col-lg-10.padding-top-1x > div.details-panel.flex-container.bottom-margin-2x > div.details-panel-item--header.flex-container > h1::text").extract()[1].strip()
        token_name_List.append(token_name)
        # Calc. Mean
        rolling_avg_volume_monthly_List.append(round(sum(temp_volume_monthly_List)/len(temp_volume_monthly_List)))  # Append
        rolling_avg_volume_weekly_List.append(round(sum(temp_volume_weekly_List) / len(temp_volume_weekly_List)))  # Append
        # Name Rank Pairs
        try:
            scraped_rank_List.append(Name_Rank_pairs[token_name])
        except:
            scraped_rank_List.append(10000)
        
        print()
        print('Rolling Avg. Monthly List: ', rolling_avg_volume_monthly_List)
        print()


    """
    Run after the Scrapy is done scraping/crawling
    """
    def closed( self, reason ):
        # Get Time stamp for market cap
        timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer
        
        ### Sanity Check
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print('Name: ',len(token_name_List))
        print('Ticker: ',len(ticker_List))
        print('Rolling Monthly: ', len(rolling_avg_volume_monthly_List))
        print('Rolling Weekly: ', len(rolling_avg_volume_weekly_List))
        print('Rank: ', len(scraped_rank_List))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        ### Append rolling average columns to MASTER_ERC_df
        # Rolling_df = pd.DataFrame()
        # Rolling_df['Ticker'] = ticker_List
        # Rolling_df['Volume: Monthly Rolling Avg'] = rolling_avg_volume_monthly_List
        # Rolling_df['Market Cap: Monthly Rolling Avg'] = rolling_avg_volume_weekly_List
    

        Rolling_df = pd.DataFrame(list(zip(token_name_List,
                                            ticker_List,
                                            rolling_avg_volume_monthly_List,
                                            rolling_avg_volume_weekly_List
                                        )),
                                    columns=['Name',
                                            'Ticker',
                                            'Daily Volume ($): Last Month Avg',
                                            'Daily Volume ($): Last Week Avg'],
                                    index=scraped_rank_List)
        Rolling_df.index.name = "CMC Rank" + timeStamp  # Rename Index

        # Sort DataFrame by Index
        Rolling_df=Rolling_df.sort_index() # Sort by CMC Rank (index)

        print(Rolling_df)

        ### Create new Tab in "MASTER ERC-20.xlsx"
        fileName =  "MASTER-1000" + timeStamp + ".xlsx"
        file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/Data/" + fileName
        writer_HardDrive = pd.ExcelWriter(file_path_HardDrive, engine='openpyxl')

        # Write to new sheet in existing workbook
        book_HardDrive = load_workbook(file_path_HardDrive)
        writer_HardDrive.book = book_HardDrive

        # Write Sheet
        Rolling_df.to_excel(writer_HardDrive, startrow= 0 , index=True, sheet_name= 'Rolling Averages' + timeStamp) # write to "MASTER-Ercot.xlsx" spreadsheet

        writer_HardDrive.save()
        writer_HardDrive.close()








