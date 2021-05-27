# -*- coding: utf-8 -*-
"""
Created on Thu May 27 14:22:11 2021

"""

import edgar_downloader as d
import edgar_cleaner as c
import ref_data as r
import edgar_sentiment_wordcount as swc

import argparse
import os

parser = argparse.ArgumentParser(description='demo of command line argument parsing')      


parser.add_argument("--ticker_list", default='AAPL,MSFT', type=str, help='provide a list of tickers seperated by , e.g. "MSFT,AAPL"')

args = parser.parse_args()

#so args.ticker_list is a string
tl = str(args.ticker_list).split(',')

cwd = os.getcwd()

# specifying file paths
raw = cwd+'/Raw_Data'
cln = cwd+'/Clean_Data'
out = cwd


if __name__ == '__main__':
    # HERE RUN MODULES IN ORDER TO PRODUCE A DEMO, GIVEN THE SPECIFIED ENTERIES
    # -- will put the files in the cwd
    
    d.download_files_10k(tl, raw)
    
    c.write_clean_html_text_files(raw, cln)
    
    swc.write_document_sentiments(cln, out)
    
    
    #### END #####








