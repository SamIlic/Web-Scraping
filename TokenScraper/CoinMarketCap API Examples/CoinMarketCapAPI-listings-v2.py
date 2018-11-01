"""
This File uses the CoinMarketCap API to scrape listings data

This script displays all active crypto listings
    - Rank
    - Name
    - Ticker
    - website slug (used for building URLs)
    - Last timestamp the info was updated on CoinMarketCap

Run code in Terminal via: "python CoinMarketCapAPI-listings-v2.py"


NOTE: public API will be taken down Dec 4, 2018 --> need to migrate to private API
"""

import json
import requests
from datetime import datetime

listings_url = 'https://api.coinmarketcap.com/v2/listings/'

request = requests.get(listings_url)
results = request.json()

# print(json.dumps(results, sort_keys=True, indent=4))

data = results['data']

print()
for currency in data:
    rank = currency['id']
    name = currency['name']
    symbol = currency['symbol']
    print(str(rank) + ': ' + name + ' (' + symbol + ')')
print()

last_updated_timestamp = results['metadata']['timestamp']
last_updated_string = datetime.fromtimestamp(last_updated_timestamp).strftime('%B %d, %Y at %I:%M%p')
print('This information was updated on ' + last_updated_string + '.')
print()












