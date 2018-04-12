from datetime import datetime, timedelta
import pandas_datareader as pdr
import pandas as pd


def download_ticker(ticker, look_back):
    ticker = ticker.upper()
    key = ticker + ' {} '.format(int(look_back))
    cache = get_cache()
    if key in cache.keys():
        return cache[key]
    today = datetime.today()
    data = pdr.DataReader(ticker,data_source = 'iex', start = today - timedelta(days = look_back), end = today , retry_count= 3, pause= 1)
    data = data.reset_index()
    cols = []
    for column in data.columns:
        cols.append(column.lower().title())
    data.columns = cols
    data['Date'] = pd.to_datetime(data["Date"])
    data = data.set_index('Date')
    cache[key] = data['Close'] 
    return cache[key]

def get_cache():
    global cache
    global today
    if datetime.today().day != today.day:
        del cache

    try:
        cache
    except NameError:
        cache = {}
    return cache

def download_tickers(tickers, look_back):
    today = pd.to_datetime(datetime.today().strftime('%Y-%B-%d'))
    final = pd.DataFrame(index = pd.date_range(today- timedelta(days = look_back), today))
    for ticker in tickers:
        ticker = ticker.strip()
        if '-' in ticker:
            a, b = ticker.split('-')
            a = download_ticker(a.strip())
            b = download_ticker(b.strip())
            cache[ticker] = a - b
            
        final[ticker] = download_ticker(ticker, look_back)
    return final


today = datetime.today()

