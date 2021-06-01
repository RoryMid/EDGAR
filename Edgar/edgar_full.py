# -*- coding: utf-8 -*-
"""
Created on Thu May 27 14:34:04 2021

"""


import edgar_downloader as d
import edgar_cleaner as c
import ref_data as r
import edgar_sentiment_wordcount as swc
import joins as j
import analysis as a

import os


cwd = os.getcwd()

# specifying file paths
raw = cwd+'/Raw_Data'
cln = cwd+'/Clean_Data'
out = cwd

# making directories
if not os.path.exists(raw):
    os.makedirs(raw)
if not os.path.exists(cln):
    os.makedirs(cln)


if __name__ == '__main__':
    # HERE RUN MODULES IN ORDER TO PRODUCE A DEMO, GIVEN THE SPECIFIED ENTERIES
    # -- will put the files in the cwd
    
    d.download_files_10k(r.get_sp100(), raw)
    print('Now Cleaning...')
    c.write_clean_html_text_files(raw, cln)
    print('Now Counting the sentiment words...')
    swc.write_document_sentiments(cln, out)
    
    print('Producing table of word count and financial data')
    j.merge_wordcounts_and_yahoo(cwd)
    
    print('Analysis: Producing graphs + saving regression analysis table')
    a.run_analysis()
    
    print('END')
    
    
    #### END #####
    
    

    #### END #####





