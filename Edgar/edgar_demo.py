# -*- coding: utf-8 -*-
"""
Created on Thu May 27 14:22:11 2021

"""


import argparse
parser1 = argparse.ArgumentParser(description='demo of command line argument parsing')      


parser1.add_argument("--ticker_list", default='AAPL,MSFT', type=str, help='provide a list of tickers seperated by , e.g. "MSFT,AAPL"')

args = parser1.parse_args()

import sys


sys.argv = [sys.argv[2]]


import edgar_downloader as d
import edgar_cleaner as c
import ref_data as r
import edgar_sentiment_wordcount as swc
import joins as j
import analysis as a

import argparse
import os

import re



#so args.ticker_list is a string
tl = str(sys.argv).split(',')

# removing stuff
for t in tl:
    t = re.sub("[^a-zA-Z]+", "", t)

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
    #so args.ticker_list is a string
   
    
    argu = []
    # removing stuff
    for s in tl:
        argu.append(''.join([i for i in s if i.isalpha()]))

    
    
    print(argu)
    d.download_files_10k(argu, raw)
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








