import pandas as pd
import praw
from datetime import datetime, timedelta
import pandas_datareader as pdr
from statsmodels import regression
import statsmodels
import sqlite3
import string

def download_ticker(ticker):
    global cache
    try:
        cache
    except NameError:
        cache = {}
    if ticker in cache.keys():
        return cache[ticker]
    today = datetime.today()
    data = pdr.DataReader(ticker,data_source = 'iex', start = today - timedelta(days = 500), end = today , retry_count= 3, pause= 1)
    data = data.reset_index()
    cols = []
    for column in data.columns:
        cols.append(column.lower().title())
    data.columns = cols
    data['Date'] = pd.to_datetime(data["Date"])
    data = data.set_index('Date')
    cache[ticker] = data['Close'] 
    return cache[ticker]

def delete_cache():
    global cache
    del cache
    cache = {}
    return 


def get_correlation(ticker):
    ticker = ticker.upper()
    spy = download_ticker('SPY')
    other = download_ticker(ticker)
    spy = spy.pct_change()
    other = other.pct_change()
    final = pd.DataFrame(index = other.index)
    final['OTHER'] = other
    final['SPY'] = spy
    final = final.dropna()
    
    X = final['SPY'].values
    X = statsmodels.tools.add_constant(X)
    y = final['OTHER'].values
    
    model = regression.linear_model.OLS(y, X).fit()
    return model

def multi_factor_model(predictors_, ticker):
    ticker = ticker.upper()
    predictors = {}
    data = download_ticker(ticker)
    final = pd.DataFrame(index = data.index)
    final[ticker] = data
    predictors = []
    for predictor in predictors_:
        predictor = predictor.upper()
        predictors.append(predictor)
        if '-' in predictor:
            a, b = predictor.split('-')
            a = download_ticker(a.strip())
            b = download_ticker(b.strip())
            cache[predictor] = a - b
        final[predictor] = download_ticker(predictor)
        
    final = final.dropna().pct_change().dropna()
    
    X = final[predictors].values
    X = statsmodels.tools.add_constant(X)
    y = final[ticker].values
    
    model = regression.linear_model.OLS(y, X).fit()
    return model
    
def create_result(model, ticker):
    text = ''
    def add_line(words, text):
        text = text + '\n\n' + words
        return text

    text = add_line(' Market exposure for {} \n'.format(ticker), text)
    text = add_line('Are these results complete gibberish? (p >= 0.05): {}'.format(model.f_pvalue > 0.05), text)
    text = add_line('Alpha value of Ticker: {} - Gibberish? {}'.format(
            model.params[0], model.pvalues[0] > 0.05), text)
    
    text = add_line('Beta value of Ticker to market: {} - Gibberish? {}'.format(
            model.params[1], model.pvalues[1] > 0.05), text)
    return text

def make_table(table):
    csv = []
    for row in table:
        row_data = []
        for cell in row:
            temp = cell.data.replace(',','.').replace('|', '!')
            temp = ' {} '.format(temp)
            row_data.append(temp)
        csv.append(','.join(row_data))
    max_len = 0
    
    for row in csv:
        x = len(row.split(','))
        if x > max_len:
            max_len = x
    
    header = ''
    if len(csv[0].split(',')) < max_len:
        header = str(csv[0])
        csv = csv[1:]
    
    csv.insert(1, '|'.join([':--']*max_len))
    csv[0] = csv[0].replace(' ', '.')
    csv = '\n'.join(csv)
    csv = csv.replace(',', '|')
    return header +'\n\n' + csv

def to_reddit_table(model, ticker):
    tables = model.summary().tables
    text = ''
    for table in tables:
        text = text +   ' \n\n __  \n\n  ' + make_table(table)
    return text



def create_table():
    with sqlite3.connect('database.db') as con:
        sql = '''    CREATE TABLE IF NOT EXISTS replied_comments (
            comment_name TEXT PRIMARY KEY NOT NULL
        )'''
        con.execute(sql)
        
    return 

def is_replied(thing):
    create_table()
    name = thing.fullname
    with sqlite3.connect('database.db') as con:
        results = pd.read_sql("select * from replied_comments where comment_name = '{}'".format(name), con)
        if len(results) >= 1:
            return True
    return False
        
def save_replied(thing):
    create_table()
    name = thing.fullname
    with sqlite3.connect('database.db') as con:
        con.execute(" INSERT INTO replied_comments(comment_name) values('{}')".format(name))

def download_tickers():
    try:
        data = pd.read_json('tickerlist.json')
        return data
    except ValueError:
        pass
    nyse = pd.read_csv('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download')
    nasdaq = pd.read_csv('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download')
    amex =  pd.read_csv('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download')
    data = nyse.append(nasdaq).append(amex)
    data['Symbol']= data['Symbol'].str.replace(' ', '')
    data = data.set_index('Symbol')
    data = data[~data.index.duplicated()]

    del data['Unnamed: 9']
    data['table_name'] = '_'+ data.index + '_'
    data.to_json('tickerlist.json')
    return data

def figure_out_command(words):
    words = words.lower()
    commands = ['regress(']
    if 'abathor:' not in words:
        return False
    

    for command in commands:
        if command in words.lower():
            
            start = len(command) + words.index(command)
            end = words.find('!')
            tickers = words[int(start): int(end)].split(',')
            final_tickers = []
            
            for ticker in tickers:
                ticker = ticker.strip().upper()
                for punc in string.punctuation:
                    if punc not in '+-/*':
                        ticker = ticker.replace(punc, '')
                    
                final_tickers.append(ticker)
            if len(final_tickers) < 2:
                return False
            return command, final_tickers, end
    return False


def respond_to_text(text):
    command = figure_out_command(text.lower())
    if type(command) == type(False):
        raise ValueError('No valid command')
    command, tickers, end = command
    
    if command == 'regress(':
        model = multi_factor_model(tickers[1:], tickers[0])
        text = to_reddit_table(model, tickers[0])
        return text





def main_loop(subreddit):
    today = datetime.today()
    
    for comment in subreddit.stream.comments():
        if datetime.today().day != today.day:
            today = datetime.today()
            delete_cache()
        comment_text = comment.body.lower()
        if 'abathor:' in comment_text:
            print(comment_text)
            if not is_replied(comment):
                try:
                    response = respond_to_text(comment_text)
                except Exception as e:
                    response = 'Error: ' + (str(e))
                    
                text = '''I'm Abathor, a bot that runs on u/2yan's account and provides correlation figures and other statistics''' 
                text = text + '  \n\n\n  ' + response
                text = text + ' \n\n Github: https://github.com/2yan/reddit_abathor/ ' 
                comment.reply(text)
                
                print('replied')
                save_replied(comment)
                

if __name__ == '__main__':

    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit("wallstreetbets+investing+robinhood")
    cache = {}
    main_loop(subreddit)

