import numpy as np
import pandas as pd
#import seaborn as sns
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
    '''
    for i in [1,2,3,5,10]:
            sns.lmplot(x='positivity',y=f'daily_return_over_market_{i}',data = df, fit_reg = True)
            plt.xlim(0,1.5)
            plt.axhline(0)
            plt.show()
    
    plt.clf()
    for i in [1,2,3,5,10]:
            sns.lmplot(x='positivity',y=f'daily_volatility_over_market_{i}',data = df, fit_reg = True)
            plt.xlim(0,1.5)
            plt.axhline(1)
            plt.show()
    '''
    ### MAKING SOME NICE GRAPHS ###
        ## want 4 graphs: RETURNS & VOLATILITY
            ### 1 and 10 day
            
    # get rid of 7 NaNs and 1 inf (from ammendments)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    

    ##################
    #RETURNS#
    fig, ax_arr = plt.subplots(1,2, figsize=(16,10))
    colour_list = ['green','green']
    title_list = ['Returns Over Market - 1 Day','Returns Over Market - 10 Days']
    x = df['positivity']
    y_list = [df['daily_return_over_market_1'], df['daily_return_over_market_10']]
    alpha_list = [0.3, 0.3]
    
    for ax, colour, title, y, alpha in zip(ax_arr, colour_list, title_list, y_list, alpha_list):
        ax.set_ylim(-0.2, 0.2)
        ax.set_xlim(0, 2)
        ax.set_title(title)
        ax.scatter(x, y, c=colour, alpha = alpha)
        m, b = np.polyfit(x, y, 1)
        ax.plot(x, m*x + b, c='red')
        ax.set_xlabel('positivity')
        ax.set_ylabel('RoM %')
        ax.axhline(0, color='black')
        ax.axvline(0, color='black')
    fig.savefig("returns.pdf", dpi=150)


    ##################
    #VOLATILITY#
    fig, ax_arr = plt.subplots(1,2, figsize=(16,10))
    colour_list = ['blue','blue']
    title_list = ['Volatility Over Market - 1 Day','Volatility Over Market - 10 Days']
    x = df['positivity']
    y_list = [df['daily_volatility_over_market_1'], df['daily_volatility_over_market_10']]
    
    #df1 = pd.concat([df['positivity'], df['daily_volatility_over_market_1']], axis=1)
    
    for ax, colour, title, y, alpha in zip(ax_arr, colour_list, title_list, y_list, alpha_list):
        ax.set_ylim(0,500)
        ax.set_xlim(0, 2)
        ax.set_title(title)
        ax.scatter(x, y, c=colour, alpha=alpha)
        m, b = np.polyfit(x, y, 1)
        ax.plot(x, m*x + b, c='red')
        ax.set_xlabel('positivity')
        ax.set_ylabel('VoM %')
        ax.axhline(0, color='black')
        ax.axvline(0, color='black')
    fig.savefig("volatility.pdf", dpi=150)



    ''' 
    No noticeable difference between positive vs negative.
    Lots of volatility in day 1 after a 10K release - should look into this
    Need to back up with hard numbers.  Look at time of year?
    '''
    
#run_analysis()
    