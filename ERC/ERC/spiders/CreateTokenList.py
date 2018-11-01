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


class ScrapeTokenData(scrapy.Spider):
    name = 'CreateTokenList'  # Name of Script
    
    start_urls = ['https://eidoo.io/erc20-tokens-list/']
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
        values  = response.css("#col > h4:nth-child(2)").extract()
        
        tokens = [value for idx, value in enumerate(values) if idx % 4 == 0]
        marketCap = [value for idx, value in enumerate(values) if idx % 4 == 2]
        ranking = list(range(1,len(tokens) + 1))

        # Clean up 
        tokens = [item.replace("<h4>","") for item in tokens]
        tokens = [item.replace("</h4>","") for item in tokens]

        marketCap = [item.replace("<h4>","").strip() for item in marketCap]
        marketCap = [item.replace("</h4>","").strip() for item in marketCap]

        temp = [item.split(" (") for item in tokens]
        temp = pd.DataFrame(data=temp, index=ranking)
        temp.iloc[:,1] = [item.replace(")", "").strip() for item in temp.iloc[:,1]]
        temp.iloc[:,0] = [item.strip() for item in temp.iloc[:,0]]
        
        df = pd.DataFrame(data=temp, index=ranking)
        df.columns = ['ERC-20 Token', 'Ticker']
        
        # Get Time stamp for market cap
        timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer
        
        
        df['Look Up Name'] = df.iloc[:,0]
        df['Look Up Name'] = [item.lower().replace(" ", "-") for item in df['Look Up Name']]
        df['CoinMarketCap URL'] = [ ("https://coinmarketcap.com/currencies/"+item+"/") for item in df['Look Up Name']]
        df['Market Cap' + timeStamp] = marketCap

        df = df.iloc[0:200, :]

        print(df)

        ### Write .xlsx file
        fileName = "Top-ERC-20" #+ timeStamp
        file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC" + fileName + ".xlsx"
        writer_HardDrive = pd.ExcelWriter(file_path_HardDrive)  #, engine='openpyxl')
        df.to_excel(writer_HardDrive, startrow= 0 , index=True, sheet_name= 'Summary') # write to "MASTER-Ercot.xlsx" spreadsheet

        writer_HardDrive.save()
        writer_HardDrive.close()






