import pandas as pd
from statsmodels import regression
import statsmodels
import data_getter
import formatter

def multi_factor_model(predictors_, ticker):
    independant = data_getter.download_tickers(predictors_, 2*365)
    dependant = data_getter.download_tickers([ticker], 2*365)[ticker]
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
    text = formatter.model_to_reddit_table(model)
    return text
    

def correlate(ticker_list):
    data = data_getter.download_tickers(ticker_list, 2*365)
    data = data.dropna().pct_change().dropna()
    data= data.corr('spearman')
    data.index.name = 'Spearman correlation'
    data = data.apply(lambda x: round(x, 4))
    text = formatter.convert_dataframe_to_reddit_table(data)
    text = text + '\n\n' + 'Spearman Rank correlation on percentage changes of 2 years of data.' 
    return text
    
command_list = {'regress(': regress,
                         'correlate(':correlate}
