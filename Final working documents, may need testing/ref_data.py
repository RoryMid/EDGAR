# -*- coding: utf-8 -*-
"""
Created on Wed May 26 09:07:19 2021

"""

def get_sp100():
    '''
    Scrapes wikipedia page to get tickers for the S&P100 companies. Returns list.
    '''
    import requests 
    from bs4 import BeautifulSoup as bs
    
    url  = 'https://en.wikipedia.org/wiki/S%26P_100'
    r = requests.get(url)
    soup = bs(r.text, 'lxml')
    table_soup = soup.find("table",{"class":"wikitable sortable"})
    tickers = []

    row_soup = table_soup.find_all('tr')

    for row in row_soup[1:]:      
        td_soup = row.find_all('td')
        tickers.append(td_soup[0].text.replace('\n', '').replace('BRK.B','BRK-B'))
    return tickers

print(get_sp100())



def get_yahoo_data(start_date,end_date,tickers):
    '''
    Uses Yahoo financials to get pricing info on each company. Creates columns for 1, 2, 3, 5, 10 daily returns. Returns dataframe.
    '''
    from yahoofinancials import YahooFinancials
    import pandas as pd
    dftot = pd.DataFrame(columns=['formatted_date','high','low','adjclose','volume','1daily_return','2daily_return','3daily_return','5daily_return','10daily_return'])
    for i in tickers:
        try:
            yahoo_financials = YahooFinancials(i)
            historical_stock_prices = yahoo_financials.get_historical_price_data(start_date, end_date, 'daily')
            df = pd.DataFrame(historical_stock_prices[i]['prices'])
            df1 = df[['formatted_date','high','low','adjclose','volume']].copy()
            #create copy to avoid changing OG df
            mask = df1.adjclose
            #adding mask to dry up a bit 
            df1['1daily_return'] = (mask.shift(-1) - mask)/mask
            df1['2daily_return'] = (mask.shift(-2) -mask)/mask
            df1['3daily_return'] = (mask.shift(-3) - mask)/mask
            df1['5daily_return'] = (mask.shift(-5) - mask)/mask
            df1['10daily_return'] = (mask.shift(-10) - mask)/mask
            df1['ticker'] = i
            dftot = dftot.append(df1)
        except:
            print(f'{i} has no data for these dates or there is an error')

    return dftot



def get_sentiment_word_dict():
    import pandas as pd
    
    key_words = ['Negative', 'Positive', 'Uncertainty', 'Litigious', 'Constraining' \
                 , 'Superfluous', 'Interesting', 'Modal']
    
    sen_words = {}
    
    # adding in the keys
    for w in key_words:
        sen_words[w] = []
    
    
    # words will be {'Negative': [Bad, Down, etc.], etc.}
    
    # have to have Words.csv in the same working directory you are in
    url = 'https://drive.google.com/file/d/12ECPJMxV2wSalXG8ykMmkpa1fq_ur0Rf/view'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_csv(path)

    
    # now need to populate words - want to iterate through the DF and 
    # assign the column to the key appropriately
    
    # iterate through key_words
    for w in key_words:
        # now want to iterate down the column
        col = df[w]
        for index in range(len(col)):
            if col.iloc[index] != 0:
                sen_words[w].append(df['Word'].iloc[index].lower())
    
    
    return sen_words
    
    

#print(get_sentiment_word_dict())
