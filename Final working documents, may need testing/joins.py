# -*- coding: utf-8 -*-
"""
Created on Thu May 27 12:14:53 2021
@author: MattRoberts
"""

import os
import pandas as pd
from ref_data import get_yahoo_data,get_sp100
import datetime as dt

def yahoo_avg():
    pd.set_option('display.max_columns', 500)
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 100)
    tickers = get_sp100()
    df_yahoo_avg=get_yahoo_data('2001-01-01','2021-05-30',tickers)
    df_yahoo_avg['formatted_date']  = pd.to_datetime(df_yahoo_avg['formatted_date'])
    df_yahoo_avg = df_yahoo_avg.groupby('formatted_date').agg({'adjclose':'sum','volume':'sum'})
    mask = df_yahoo_avg.adjclose
    for i in [1,2,3,5,10]:
        df_yahoo_avg[f'{str(i)}daily_return_market'] = (mask.shift(-i) - mask)/mask
    return df_yahoo_avg


def merge_wordcounts_and_yahoo(output_folder):
    # To display big dataframes:
    pd.set_option('display.max_columns', 500)
    pd.set_option('expand_frame_repr', False)
    
    # Import wordcounts data from .csv file:               # Still need to make the complete csv?
    wordcounts_csv = output_folder+'/document_sentiments.csv'          # need csv file in same folder as this module :)
    df_wordcounts = pd.read_csv(wordcounts_csv)
    df_wordcounts = df_wordcounts.dropna()
    
    # Get yahoo data from ref_data_dryer module:

    tickers = get_sp100()                                            # Need to add all tickers
    df_yahoo = get_yahoo_data('2001-01-01','2021-05-30', tickers)
    
    # Convert dates to datetime format:
    df_yahoo['formatted_date']  = pd.to_datetime(df_yahoo['formatted_date'])
    df_wordcounts['FilingDate'] = pd.to_datetime(df_wordcounts.FilingDate).dt.strftime('%Y/%m/%d')
    df_wordcounts['FilingDate']  = pd.to_datetime(df_wordcounts['FilingDate'])
    
    # Merge wordcounts and yahoo:
    df_words = pd.merge_asof(df_wordcounts.sort_values('FilingDate'), df_yahoo.sort_values('formatted_date'),
                  left_on='FilingDate', right_on='formatted_date',
                  left_by = 'Symbol', right_by = 'ticker', 
                  direction = "forward"
                  )
    
    # Just some tests:
    #x = df_wordcounts[df_wordcounts.columns[0]].count()
    #y = df_words[df_words.columns[0]].count()
    #print(f'Number of rows (10-Ks) in wordcounts doc was : {x}')
    #print(f'Number of rows in the resulting dataframe is : {y}')
    #print(f'Hopefully {x} and {y} are the same number.')
    df_avg = yahoo_avg()
    df = pd.merge(df_words,df_avg,how='left',on='formatted_date')
    df.to_csv('sentiments_returns.csv', index=True, header=True)

