# -*- coding: utf-8 -*-
"""
Created on Thu May 27 14:34:04 2021

"""


import edgar_downloader as d
import edgar_cleaner as c
import ref_data as r
import edgar_sentiment_wordcount as swc

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
    
    c.write_clean_html_text_files(raw, cln)
    
    swc.write_document_sentiments(cln, out)
    
    
    #### END #####





