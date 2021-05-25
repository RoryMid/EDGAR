# -*- coding: utf-8 -*-
"""
Created on Tue May 25 18:45:22 2021

"""

import os
import get_sentiment_word_dict

def write_document_sentiments(input_folder, ouput_file):
            
    sen_words = get_sentiment_word_dict.get_sentiment_word_dict()
    
    key_words = ['Negative', 'Positive', 'Uncertainty', 'Litigious', 'Constraining' \
                 , 'Superfluous', 'Interesting', 'Modal']
    
    # MAKE EMPTY DF TO BE RETURNED 
    # SYMBOL | REPORT TYPE | FILING DATE | NEGATIVE | POSITIVE | UNCERTAINTY | LITIGOUS | CONSTRAINING | SUPERFLUOUS | INTERSETING | MODAL
        # UPDATED WITH THE SYMBOL, REPORT TYPE AND DATE
       
        
    
    for file in os.listdir(input_folder):
        
        # HAVE TO ADD A ROW TO THE DF WITH 0 IN ALL WORDS
        
        
        with open(input_folder+'/'+file, encoding="utf8") as file:

            # now for each file we want to get a list of words
            # then compare these words to the dictionary 
            
            lines = file.readlines()
            
            for line in lines:
                l = line.split()
                # l is a list of words 
                # for each word have to check if its in the dictionary
                for word in l:
                    word2 = word.lower()
                    
                    # now check if its in dictionary
                    for key in key_words:
                        
                        if word2 in sen_words[key]:
                            
                            # ADD 1 TO THE DF AT THAT POINT (KEY)
                
                
                
        
    return DF
            
            
    

write_document_sentiments( \
  r'C:\Users\AlfieCrust\OneDrive - Kubrick Group\Desktop\Training Notes\7. Python\Python Project\EdgarRipple\TestData2' \
      , '')





