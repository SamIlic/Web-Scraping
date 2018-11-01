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




class ICObench(scrapy.Spider):
    name = 'ICOBench'  # Name of Script
    
    # file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/Data/COINS.xlsx"
    file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/Data/MASTER-1000.xlsx"
    MASTER_Coin_df = pd.read_excel(file_path, sheet_name = "Summary") # read all data from "Top ERC-20"
    headers = list(MASTER_Coin_df.columns.values) # get the headers --> ERC-20 Token, Ticker, ID, CoinMarketCap URL, Market Cap (yyyy-mm-dd) 
   
    # URLs
    URLs = MASTER_Coin_df['CoinMarketCap URL']
    temp_urls = URLs.values.tolist()
    temp_urls = [url + "historical-data/" for url in temp_urls]




    print("``````````````````````````````````````````````````````````````````````````````")
    # start_urls = ['https://icobench.com/ico/tezos']  # TEST
    start_urls = temp_urls
    print("``````````````````````````````````````````````````````````````````````````````")

################################################################################################
################################################################################################

    """
    Scrape data from ICO-bench for all cryptos in MASTER-1000
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
        



    # """
    # Run after the Scrapy is done scraping/crawling
    # """
    # def closed( self, reason ):
    #     # Get Time stamp for market cap
    #     timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer
        
    #     ### Sanity Check
    #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     print('Name: ',len(token_name_List))
    #     print('Ticker: ',len(ticker_List))
    #     print('Rolling Monthly: ', len(rolling_avg_volume_monthly_List))
    #     print('Rolling Weekly: ', len(rolling_avg_volume_weekly_List))
    #     print('Rank: ', len(scraped_rank_List))
    #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
    #     ### Append rolling average columns to MASTER_ERC_df
    #     # Rolling_df = pd.DataFrame()
    #     # Rolling_df['Ticker'] = ticker_List
    #     # Rolling_df['Volume: Monthly Rolling Avg'] = rolling_avg_volume_monthly_List
    #     # Rolling_df['Market Cap: Monthly Rolling Avg'] = rolling_avg_volume_weekly_List
    

    #     Rolling_df = pd.DataFrame(list(zip(token_name_List,
    #                                         ticker_List,
    #                                         rolling_avg_volume_monthly_List,
    #                                         rolling_avg_volume_weekly_List
    #                                     )),
    #                                 columns=['Name',
    #                                         'Ticker',
    #                                         'Daily Volume ($): Monthly Rolling Avg',
    #                                         'Daily Volume ($): Weekly Rolling Avg'],
    #                                 index=scraped_rank_List)
    #     Rolling_df.index.name = "CMC Rank" + timeStamp  # Rename Index

    #     # Sort DataFrame by Index
    #     Rolling_df=Rolling_df.sort_index() # Sort by CMC Rank (index)

    #     print(Rolling_df)

    #     ### Create new Tab in "MASTER ERC-20.xlsx"
    #     # fileName = "MASTER ERC-20 Rolling" #+ timeStamp
    #     file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/Data/MASTER-1000.xlsx"
    #     writer_HardDrive = pd.ExcelWriter(file_path_HardDrive, engine='openpyxl')

    #     # Write to new sheet in existing workbook
    #     book_HardDrive = load_workbook(file_path_HardDrive)
    #     writer_HardDrive.book = book_HardDrive

    #     # Write Sheet
    #     Rolling_df.to_excel(writer_HardDrive, startrow= 0 , index=True, sheet_name= 'Rolling Averages' + timeStamp) # write to "MASTER-Ercot.xlsx" spreadsheet

    #     writer_HardDrive.save()
    #     writer_HardDrive.close()








