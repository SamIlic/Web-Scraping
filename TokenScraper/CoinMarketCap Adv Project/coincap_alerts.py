"""
# NOTE (for Sam): Run on "QSTrader" Conda Virtual Enviroment 
    > "source activate QSTrader"
    > Run via "python coincap_portfolio.py"

Summary of script
    - Need to provide a text file corresponding to alerts
        - Portfolio can pe provided as .csv or .xlsx file but then the code must be modified
    - Displays
        - Your portfolio of Crypto - called "portfolio.txt"
        - The amount of each crypto you own
        - The USD value for each crypto
        - The current price of each crypto you own
        - Change in prices for 1h, 24h, 7d (color coated)
        - Your total portfolio value 
        - Timestamp of when the data was last updated on CoinMarketCap


# NOTE: Code must be run on a Virtual Environment in order to import "prettytable" (as least this was the case for me)
"""

import os
import json
import time
import requests
from datetime import datetime

convert = 'USD'

listings_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
url_end = '?structure=array&convert=' + convert

request = requests.get(listings_url)
results = request.json()

data = results['data']

ticker_url_pairs = {}
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

print()
print("ALERTS TRACKING...")
print()

already_hit_symbols = []

while True:
    with open("alerts.txt", "r") as inp:
        for line in inp:
            ticker, amount = line.split()
            ticker = ticker.upper()
            ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end

            request = requests.get(ticker_url)
            results = request.json()

            currency = results['data'][0]
            name = currency['name']
            last_updated = currency['last_updated']
            symbol = currency['symbol']
            quotes = currency['quotes'][convert]
            price = quotes['price']

            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                os.system('say ' + name + ' hit ' + amount)
                last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')
                print(name + ' hit ' + amount + ' on ' + last_updated_string)
                already_hit_symbols.append(symbol)

    print('...')
    time.sleep(300)