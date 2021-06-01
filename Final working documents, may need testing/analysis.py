import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import statsmodels.api as sm
       # need csv file in same folder as this module :)
       

def run_analysis():
    df = pd.read_csv('sentiments_returns.csv')
    for i in [1,2,3,5,10]:
            df[f'daily_return_over_market_{str(i)}'] = df[f'{i}daily_return'] - df[f'{i}daily_return_market']
    for i in [1,2,3,5,10]:
            df[f'daily_volatility_over_market_{str(i)}'] = abs(df[f'{i}daily_return']) / abs(df[f'{i}daily_return_market'])
    df['positivity'] = df['Positive'] / df['Negative']
    
    model_lin = sm.OLS.from_formula(formula = "daily_return_over_market_1 ~ Positive + Negative + Uncertainty + Litigious + Constraining + Superfluous + Interesting + Modal", data=df)
    result_lin = model_lin.fit()
    
    text = result_lin.summary().as_csv()
    f = open('returns.csv', 'w')
    f.write(text)
    f.close()    
    
    print(result_lin.summary())
    
    '''
    Not statistically significant findings here for returns
    '''
    
    model_lin = sm.OLS.from_formula(formula = "daily_volatility_over_market_1 ~ Positive + Negative + Uncertainty + Litigious + Constraining + Superfluous + Interesting + Modal", data=df)
    result_lin = model_lin.fit()
    
    text = result_lin.summary().as_csv()
    f = open('volatility.csv', 'w')
    f.write(text)
    f.close()    
    print(result_lin.summary())
    '''
    Statistically significant affect on volatility when high count of Litigous or Interesting words. Dive deeper into this.
    '''
    
    for i in [1,2,3,5,10]:
            sns.lmplot(x='positivity',y=f'daily_return_over_market_{i}',data = df, fit_reg = True)
            plt.xlim(0,1.5)
            plt.axhline(0)
            #plt.show()
    
    plt.clf()
    for i in [1,2,3,5,10]:
            sns.lmplot(x='positivity',y=f'daily_volatility_over_market_{i}',data = df, fit_reg = True)
            plt.xlim(0,1.5)
            plt.axhline(1)
            #plt.show()
            
    
    '''
    No noticeable difference between positive vs negative.
    Lots of volatility in day 1 after a 10K release - should look into this
    Need to back up with hard numbers.  Look at time of year?
    '''
    
run_analysis()
    