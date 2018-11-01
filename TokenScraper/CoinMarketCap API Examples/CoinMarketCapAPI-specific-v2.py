"""
This File uses the CoinMarketCap API to scrape data for a specific currency
Use this scipt to interface with the API. Hence, run the code then enter the ticker info 
    that you want 

This script displays the following for a specific currency
    - Rank
    - Name
    - Ticker
    - Circulating Supply
    - Total Supply
    - Max Supply
    - Quotes
        - Price
        - 24h Volume
        - Market Cap
        - % Change 1h
        - % Change 24h
        - % Change 7d
    - Last timestamp the info was updated on CoinMarketCap

Run code in Terminal via: "python CoinMarketCapAPI-specific-v2.py"

NOTE: public API will be taken down Dec 4, 2018 --> need to migrate to private API
"""


import json
import requests
from datetime import datetime

convert = 'USD'
listings_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
url_end = '?structure=array&convert=' + convert

request = requests.get(listings_url)
results = request.json()

# print(json.dumps(results, sort_keys=True, indent=4))

data = results['data']

ticker_url_pairs = {}
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

# print(ticker_url_pairs)

while True:
    print()
    choice = input('Enter the ticker symbol of a cryptocurrency: ')
    choice = choice.upper()
    ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[choice]) + '/' + url_end
    print("ID: ", ticker_url_pairs[choice])
    request = requests.get(ticker_url)
    results = request.json()

    # print(json.dumps(results, sort_keys=True, indent=4))

    currency = results['data'][0]

    rank = currency['rank']
    name = currency['name']
    symbol = currency['symbol']

    circulating_supply = int(currency['circulating_supply'])
    total_supply = int(currency['total_supply'])

    quotes = currency['quotes'][convert]
    market_cap = quotes['market_cap']
    hour_change = quotes['percent_change_1h']
    day_change = quotes['percent_change_24h']
    week_change = quotes['percent_change_7d']
    price = quotes['price']
    volume = quotes['volume_24h']

    volume_string = '{:,}'.format(volume)
    market_cap_string = '{:,}'.format(market_cap)
    circulating_supply_string = '{:,}'.format(circulating_supply)
    total_supply_string = '{:,}'.format(total_supply)

    print()
    print(str(rank) + ': ' + name + ' (' + symbol + ')')
    print('Market cap: \t\t$' + market_cap_string)
    print('Price: \t\t\t$' + str(price))
    print('24h Volume: \t\t$' + str(volume) + '%')
    print('Hour change: \t\t' + str(hour_change) + '%')
    print('Day change: \t\t' + str(day_change) + '%')
    print('Week change: \t\t' + str(week_change) + '%')
    print('Circulating supply: \t' + circulating_supply_string)
    print('Total supply: \t\t' + total_supply_string)
    print('Percentage circulating: ' + str(int(circulating_supply / total_supply * 100)) + '%')
    print()

    last_updated_timestamp = results['metadata']['timestamp']
    last_updated_string = datetime.fromtimestamp(last_updated_timestamp).strftime('%B %d, %Y at %I:%M%p')
    print('This information was updated on ' + last_updated_string + '.')
    print()

    choice = input('Again? (y/n): ')

    if choice == 'n':
        break












