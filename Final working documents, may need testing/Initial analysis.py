import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
       # need csv file in same folder as this module :)
df = pd.read_csv('sentiments_returns.csv')
for i in [1,2,3,5,10]:
        df[f'{str(i)}daily_return_over_market'] = df[f'{i}daily_return'] - df[f'{i}daily_return_market']
for i in [1,2,3,5,10]:
        df[f'{str(i)}daily_volatility_over_market'] = abs(df[f'{i}daily_return']) / abs(df[f'{i}daily_return_market'])
df['positivity'] = df['Positive'] / df['Negative']
for i in [1,2,3,5,10]:
        sns.lmplot(x='positivity',y=f'{i}daily_return_over_market',data = df, fit_reg = True)
        plt.xlim(0,1.5)
        plt.axhline(0)
        plt.show()

plt.clf()
for i in [1,2,3,5,10]:
        sns.lmplot(x='positivity',y=f'{i}daily_volatility_over_market',data = df, fit_reg = True)
        plt.xlim(0,1.5)
        plt.axhline(1)
        plt.show()
'''
No noticeable difference between positive vs negative.
Lots of volatility in day 1 after a 10K release - should look into this
Need to back up with hard numbers.  Look at time of year?
'''