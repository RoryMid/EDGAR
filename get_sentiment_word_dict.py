# -*- coding: utf-8 -*-
"""
Created on Tue May 25 13:46:01 2021

@author: AlfieCrust
"""

import pandas as pd

def get_sentiment_word_dict():
    
    key_words = ['Negative', 'Positive', 'Uncertainty', 'Litigious', 'Constraining' \
                 , 'Superfluous', 'Interesting', 'Modal']
    
    sen_words = {}
    
    # adding in the keys
    for w in key_words:
        sen_words[w] = []
    
    
    # words will be {'Negative': [Bad, Down, etc.], etc.}
    
    # have to have Words.csv in the same working directory you are in
    df = pd.read_csv('Words.csv')
    
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