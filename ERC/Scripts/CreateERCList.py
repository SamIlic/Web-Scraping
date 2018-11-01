# -*- coding: utf-8 -*-
import scrapy # needed to scrape
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import xlrd   # used to easily import xlsx file 
import json
import re
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import datetime



### Initialize List Variables
token_name_List = list()
erc_List = list()
is_erc_List = list()

# Get Time stamp for market cap
timeStamp = str(datetime.datetime.today().strftime(' (%Y-%m-%d)')) # Today, as an Integer

# Open .xlsx
file_path_COIN = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/Data/COINS.xlsx"
#COIN_df = pd.read_excel(file_path_COIN, sheet_name = "ERC") # read all data from "Top ERC-20"
COIN_df = pd.read_excel(file_path_COIN, sheet_name = "ERC-20 (2018-08-10)") # read all data from "Top ERC-20"
file_path_MASTER = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/Data/MASTER-1000.xlsx"
MASTER_df = pd.read_excel(file_path_MASTER, sheet_name = "API Data") # read all data from "Top ERC-20"

COIN_df = pd.DataFrame(COIN_df)
MASTER_df = pd.DataFrame(MASTER_df)

### TOP 199 ERC-20 TOKENS AS OF (2018-08-10)
coin_names = MASTER_df['Name'].values
erc_List = COIN_df['Top 200 ERC-20 Tokens'].values

# coin_names = [coi.strip().lower() for coi in coin_names]
# erc_List = [tok.strip().lower() for tok in erc_List]

for coin_name in coin_names: # Rank 1-1000
    if coin_name in erc_List:
        is_erc_List.append(1)  # Is Top 200 ERC
    else:
        is_erc_List.append(0)  # Not Top 200 ERC


rank = list(range(1,1001))
ERC_df = pd.DataFrame(list(zip(coin_names,
                               is_erc_List
                        )),
                        columns=['Name',
                                 'Top 200 ERC-20?'
                        ],
                        index=rank)
ERC_df.index.name = "CMC Rank" + timeStamp  # Rename Index
print(ERC_df)

### Create new Tab in "MASTER-1000.xlsx"
fileName = "MASTER ERC-20 Rolling" #+ timeStamp
file_path_HardDrive = r"/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/ERC/Data/MASTER-1000.xlsx"
writer_HardDrive = pd.ExcelWriter(file_path_HardDrive, engine='openpyxl')

# Write to new sheet in existing workbook
book_HardDrive = load_workbook(file_path_HardDrive)
writer_HardDrive.book = book_HardDrive

# Write Sheet
ERC_df.to_excel(writer_HardDrive, startrow= 0 , index=True, sheet_name= 'ERC' + timeStamp) # write to "MASTER-Ercot.xlsx" spreadsheet

writer_HardDrive.save()
writer_HardDrive.close()








