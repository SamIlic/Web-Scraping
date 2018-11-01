"""
This File uses the CoinMarketCap API to scrape Global Coin Data

This file 
    - Active Currencies
    - Active Markets
    - Bitcoin Market Cap % of Global Market Cap
    - Quotes
        - Global Market Cap
        - Global Volume 24h
    - Last timestamp the info was updated on CoinMarketCap

Run code in Terminal via: "python CoinMarketCapAPI-global-v2.py"

NOTE: public API will be taken down Dec 4, 2018 --> need to migrate to private API
"""

import json
import requests
from datetime import datetime

# Set the currency
currency = 'USD'

global_url = 'https://api.coinmarketcap.com/v2/global/' + '?convert=' + currency

# Gets the global_url and puts all of that json data inside of request
request = requests.get(global_url) 
results = request.json()  # no format this data

# Print the json format of the data that we are accessing
#print(json.dumps(results, sort_keys=True, indent=4))

data = results['data']
active_currencies = data['active_cryptocurrencies']
active_markets = data['active_markets']
bitcoin_percentage = data['bitcoin_percentage_of_market_cap']
last_updated_timestamp = data['last_updated']
global_cap = int(data['quotes'][currency]['total_market_cap'])
global_volume = int(data['quotes'][currency]['total_volume_24h'])

# Convert numbers frormat to include commas
active_currencies_string = '{:,}'.format(active_currencies)
active_markets_string = '{:,}'.format(active_markets)
global_cap_string = '{:,}'.format(global_cap)
global_volume_string = '{:,}'.format(global_volume)

last_updated_string = datetime.fromtimestamp(last_updated_timestamp).strftime('%B %d, %Y at %I:%M%p')

print()
print('There are currently ' + active_currencies_string + ' active currencies and ' + active_markets_string + ' active markets.')
print('The global market cap is $' + global_cap_string + ' and the 24h volume is $' + global_volume_string + '.')
print('Bitcoin\'s market cap makes up ' + str(bitcoin_percentage) + '% of the global market cap.')
print()
print('This information was updated on ' + last_updated_string + '.')
print()













