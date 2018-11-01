"""
# NOTE (for Sam): Run on "QSTrader" Conda Virtual Enviroment 
    > "source activate QSTrader"
    > Run via "python coincap_p5.py"

Summary of script
    - This script will 

# NOTE: Code must be run on a Virtual Environment in order to import "prettytable" (as least this was the case for me)
"""

import xlsxwriter
import requests
import json

start = 1
f = 1

# open excel workbooks
crypto_workbook = xlsxwriter.Workbook('cryptocurrencies.xlsx')

# add a sheet
crypto_sheet = crypto_workbook.add_worksheet()

# add headers to the sheet
crypto_sheet.write('A1',"Rank")
crypto_sheet.write('B1',"Name")
crypto_sheet.write('C1',"Symbol")
crypto_sheet.write('D1',"Market Cap")
crypto_sheet.write('E1',"Price")
crypto_sheet.write('F1',"24h Volume")
crypto_sheet.write('G1',"Hour Change")
crypto_sheet.write('H1',"Day Change")
crypto_sheet.write('I1',"Week Change")

for i in range(10):
    ticker_url = 'https://api.coinmarketcap.com/v2/ticker/?structure=array&start=' + str(start)
    request = requests.get(ticker_url)
    results = request.json()
    data = results['data']
    for currency in data:
        rank = currency['rank']
        name = currency['name']
        symbol = currency['symbol']
        quotes = currency['quotes']['USD']
        market_cap = quotes['market_cap']
        hour_change = quotes['percent_change_1h']
        day_change = quotes['percent_change_24h']
        week_change = quotes['percent_change_7d']
        price = quotes['price']
        volume = quotes['volume_24h']

        volume_string = '{:,}'.format(volume)
        market_cap_string = '{:,}'.format(market_cap)


        crypto_sheet.write(f,0,rank)
        crypto_sheet.write(f,1,name)
        crypto_sheet.write(f,2,symbol)
        crypto_sheet.write(f,3,'$' + market_cap_string)
        crypto_sheet.write(f,4,'$' + str(price))
        crypto_sheet.write(f,5,'$' + volume_string)
        crypto_sheet.write(f,6,str(hour_change) + '%')
        crypto_sheet.write(f,7,str(day_change) + '%')
        crypto_sheet.write(f,8,str(week_change) + '%')
        f += 1

    start += 100

crypto_workbook.close()