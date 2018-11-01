# -*- coding: utf-8 -*-
import scrapy # needed to scrape
import xlrd   # used to easily import xlsx file 
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import datetime
from datetime import timedelta


class ScrapeCoinMarketCapData(scrapy.Spider):
    name = 'CoinMarketCapDataBot'  # Name of Script

    ### Open "Top ERC-20 Tokens (date)" --> turn into DataFrame
    
    global df   #make df global/public
    # df = pd.read_csv(path + 'Top ERC-20 Tokens (2018-08-05).csv', header=0, index_col=0)

    ### 1) Open Top ERC-20 Tokens File
    file_path = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/TokenScraper/"
    # top_ERC_df = pd.read_csv(file_path, header=0,index_col=0)  # for .csv
    top_ERC_df = pd.read_excel(file_path, sheetname = "Summary") # read all data from "Top ERC-20"
    headers = list(top_ERC_df.columns.values) # get the headers --> ERC-20 Token, Ticker, ID, CoinMarketCap URL, Market Cap (yyyy-mm-dd) 
    top_ERC_df = pd.DataFrame(top_ERC_df) # convert top_ERC_df to a DateFrame



    ### Clean DataFrame
    df = pd.DataFrame(top_ERC_df) # convert df to a Date Frame
    headers = list(df.columns.values) # get the headers 
    urls = df.iloc[:,3]
    print(headers)

    
    start_urls = urls
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
        
        ### Scrape table Headers and Values (energy prices)
        #values  = response.css("#col > h4:nth-child(2)").extract()
        marketCap = response.css("body > div.container.main-section > div > div.col-lg-10.padding-top-1x > div.details-panel.flex-container.bottom-margin-2x > div.details-panel-item--marketcap-stats.flex-container > div:nth-child(1) > div > span:nth-child(1) > span:nth-child(1)::text").extract()
        volume24h = response.css("body > div.container.main-section > div > div.col-lg-10.padding-top-1x > div.details-panel.flex-container.bottom-margin-2x > div.details-panel-item--marketcap-stats.flex-container > div:nth-child(2) > div > span:nth-child(1) > span:nth-child(1)::text").extract()
        circulatingSupply = response.css("body > div.container.main-section > div > div.col-lg-10.padding-top-1x > div.details-panel.flex-container.bottom-margin-2x > div.details-panel-item--marketcap-stats.flex-container > div:nth-child(3) > div > span::text").extract()        
        totalSupply = response.css("body > div.container.main-section > div > div.col-lg-10.padding-top-1x > div.details-panel.flex-container.bottom-margin-2x > div.details-panel-item--marketcap-stats.flex-container > div:nth-child(4) > div > span::text").extract()
        rank = response.css("body > div.container.main-section > div > div.col-lg-10.padding-top-1x > div.details-panel.flex-container.bottom-margin-2x > ul > li:nth-child(1) > span.label.label-success::text").extract()
        

        # Get Time stamp for market cap
        timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer
        

        #print(df)

        """
        # Create .xlsx file for any Stock data from any date from Yahoo Finance
        """
        # fileName = "TopERC"
        # ### Write to CSV
        # filePath  = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/TokenScraper/" + fileName + ".csv"  # file path 
        # df.to_csv(filePath)










