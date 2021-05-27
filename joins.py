# -*- coding: utf-8 -*-
"""
Created on Thu May 27 12:14:53 2021
@author: MattRoberts
"""

import os
import pandas as pd
from ref_data_dryer import get_yahoo_data
import datetime as dt

def merge_wordcounts_and_yahoo():
    # To display big dataframes:
    pd.set_option('display.max_columns', 500)
    pd.set_option('expand_frame_repr', False)
    
    # Import wordcounts data from .csv file:               # Still need to make the complete csv?
    wordcounts_csv = "document_sentiments_v2.csv"          # need csv file in same folder as this module :)
    df_wordcounts = pd.read_csv(wordcounts_csv)
    df_wordcounts = df_wordcounts.dropna()
    
    # Get yahoo data from ref_data_dryer module:
    tickers = ['AAPL']                                              # Need to add all tickers
    df_yahoo = get_yahoo_data('1980-01-01','2021-01-01', tickers)
    
    # Convert dates to datetime format:
    df_yahoo['formatted_date']  = pd.to_datetime(df_yahoo['formatted_date'])
    df_wordcounts['FilingDate'] = pd.to_datetime(df_wordcounts.FilingDate).dt.strftime('%Y/%m/%d')
    df_wordcounts['FilingDate']  = pd.to_datetime(df_wordcounts['FilingDate'])
    
    # Make calendar of all days, left join to yahoo, forward fill
    df_calendar = pd.DataFrame({'date':pd.date_range('1980-01-01', '2021-01-01')})
    df_daily_yahoo = pd.merge(df_calendar, df_yahoo, how='left',
                              left_on='date', right_on='formatted_date')
    df_daily_yahoo = df_daily_yahoo.ffill()
    df_daily_yahoo = df_daily_yahoo.bfill()
    
    # Merge wordcounts and yahoo:
    df = pd.merge(df_wordcounts, df_daily_yahoo, how='left',
                  left_on=['Symbol', 'FilingDate'], right_on=['ticker', 'date'])

    print(df)
    
    # Just some tests:
    x = df_wordcounts[df_wordcounts.columns[0]].count()
    y = df[df.columns[0]].count()
    print(f'Number of rows (10-Ks) in wordcounts doc was : {x}')
    print(f'Number of rows in the resulting dataframe is : {y}')
    print(f'Hopefully {x} and {y} are the same number.')

    return(df)

merge_wordcounts_and_yahoo()
