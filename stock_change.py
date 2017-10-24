#!/usr/bin/python3

from collections import OrderedDict
import requests
import sys
import json
from datetime import date

if len(sys.argv) != 2:
  print("Usage: stock_alert.py <stock symbol>")
  exit()

payload = {'function': 'TIME_SERIES_DAILY', 'symbol': sys.argv[1],
  'outputsize': 'compact', 'apikey': '--your-free-api-key-here--'}
r = requests.get('https://www.alphavantage.co/query', params=payload)
obj = json.loads(r.text, object_pairs_hook=OrderedDict)

#print(r.url)
today = date.today().strftime("%Y-%m-%d")
# see if we can find data from today
latestEntry = list(obj['Time Series (Daily)'].keys())[0]
if not latestEntry == today:
  # we have no data for today
  print("N/A")
  exit()

# find previous day data (could be yesterday, could be another time in case of holidays or weekends)
for el in obj['Time Series (Daily)']:
  if el == today:
    continue  #ignore
  else:
# we got it!
    prevDayClose = float(obj['Time Series (Daily)'][el]['4. close'])
    currentClose = float(obj['Time Series (Daily)'][latestEntry]['4. close'])
    diff = (currentClose - prevDayClose) / prevDayClose * 100

    sign = ""
    if diff > 0:
      sign = "+"

    print(sign + str(round(diff, 2)) + "%")
    break

