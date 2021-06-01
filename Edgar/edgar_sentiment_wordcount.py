# -*- coding: utf-8 -*-
"""
Created on Tue May 25 18:45:22 2021

"""

import os
import ref_data as r
import pandas as pd

import argparse

parser = argparse.ArgumentParser(description='demo of command line argument parsing')

def write_document_sentiments(input_folder, output_folder):
            
    sen_words = r.get_sentiment_word_dict()
    
    key_words = ['Negative', 'Positive', 'Uncertainty', 'Litigious', 'Constraining' \
                 , 'Superfluous', 'Interesting', 'Modal']
    
    # MAKE EMPTY DF TO BE RETURNED 
    # SYMBOL | REPORT TYPE | FILING DATE | NEGATIVE | POSITIVE | UNCERTAINTY | LITIGOUS | CONSTRAINING | SUPERFLUOUS | INTERSETING | MODAL
        # UPDATED WITH THE SYMBOL, REPORT TYPE AND DATE
    column_names = ['Symbol', 'ReportType', 'FilingDate', 'Negative', 'Positive', 'Uncertainty', \
                    'Litigious', 'Constraining', 'Superfluous', 'Interesting', 'Modal']
    df = pd.DataFrame(columns = column_names)
    
    # index to count which row we are on
    current_df_row = 0
    
    for file in os.listdir(input_folder):
        
        # HAVE TO ADD A ROW TO THE DF WITH 0 IN ALL WORDS
    
        # extract first three columns from this and add row
        file_name = file.split('_') # 0, 1 ,2
        file_name[2] = file_name[2][0:11]
        # now add row
        new_row = {'Symbol':file_name[0], 'ReportType':file_name[1], 'FilingDate':file_name[2], \
                   'Negative':0, 'Positive':0, 'Uncertainty':0, 'Litigious':0, 'Constraining':0, 'Superfluous':0, 'Interesting':0, 'Modal':0}
        df = df.append(new_row, ignore_index=True)
        #print(df)
        print('Counting:',file)
        
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
                            df[key].iloc[current_df_row] += 1
                        
                        '''
                        # now iterate through sen_words[key]
                        for sen_word in sen_words[key]:
                        
                            if sen_word in word2:
                                # if we wanted to remove punctuation --> iterate through the list at this key and use 'in' 
                                # want to iterate through sen_words[key] [LIST] and for each word see if it is in the word2
                            
                                # ADD 1 TO THE DF AT THAT POINT (KEY)
                                df[key].iloc[current_df_row] += 1
                        '''
                
        current_df_row += 1 # add one to the row index when moving on to the next file            
        
    # and write to file
    df.to_csv(output_folder+'/document_sentiments.csv', index=True, header=True)
    

###################################      
            
    
parser.add_argument("--input_folder", type=str, help='provide a path for the input folder containing html files')
parser.add_argument("--output_folder", type=str, help='provide a destination folder path')

args = parser.parse_args()


if __name__ == '__main__':
    write_document_sentiments(args.input_folder, args.output_folder) 




