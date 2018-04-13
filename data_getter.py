from datetime import datetime, timedelta
import pandas_datareader as pdr
import pandas as pd



def multi_ticker_download(ticker, start, end):
    ticker = ticker.upper()
    if  '_FRED_' in ticker:
        ticker = ticker.replace('_FRED_', '')
        data = pdr.get_data_fred(ticker, start, end)
        final = pd.DataFrame(index = pd.date_range(start, end))
        final.index.name = ticker
        final['Date'] = final.index
        final['Close'] = data
        final['Close'] = final['Close'].ffill()
        return final
    data = pdr.DataReader(ticker,data_source = 'iex', start =start , end =end , retry_count= 3, pause= 1)
    return data

def download_ticker(ticker, look_back):
    
    ticker = ticker.upper()
    key = ticker + ' {} '.format(int(look_back))
    cache = get_cache()
    if key in cache.keys():
        return cache[key]
    today = pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))
    data = multi_ticker_download(ticker, today - timedelta(days = look_back), today )
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
        ticker = ticker.upper()
        ticker = ticker.strip()
        if '-' in ticker:
            a, b = ticker.split('-')
            a = download_ticker(a.strip(), look_back)
            b = download_ticker(b.strip(), look_back)
            cache[ticker + ' {} '.format(look_back)] = a - b
            
        final[ticker] = download_ticker(ticker, look_back)
    return final


today = datetime.today()

