import pandas as pd
from datetime import datetime, timedelta
import pandas_datareader as pdr
from statsmodels import regression
import statsmodels
import data_getter
import formatter

def multi_factor_model(predictors_, ticker):
    independant = data_getter.download_tickers(predictors_, 365)
    dependant = data_getter.download_tickers([ticker], 365)[ticker]
    print
    final = pd.DataFrame(index = dependant.index)
    final[independant.columns] = independant[independant.columns]
    final[dependant.name] = dependant
    
    final = final.dropna().pct_change().dropna()

    X = final[independant.columns].values
    X = statsmodels.tools.add_constant(X)
    y = final[dependant.name].values
    
    model = regression.linear_model.OLS(y, X).fit()
    return model

def regress(ticker_list):
    model =  multi_factor_model(ticker_list[1:], ticker_list[0])
    text = formatter.to_reddit_table(model)
    return text
    
    
command_list = {'regress(': regress}
