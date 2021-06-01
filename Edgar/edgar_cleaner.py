# -*- coding: utf-8 -*-
"""
Created on Tue May 25 18:54:49 2021


"""
import argparse
import re
from bs4 import BeautifulSoup
import os

parser = argparse.ArgumentParser(description='demo of command line argument parsing')


def clean_html_text(html_text):
    '''
    Takes a html file and returns just the text
    '''
    with open(html_text, 'r', encoding = 'utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
        soup = soup.getText()
        soup = re.sub('[^A-Za-z0-9 ]+', '', soup)
    return soup    
    

def write_clean_html_text_files(input_folder, dest_folder):
    '''
    For each html file in the input folder, get the text and then saves this in destination folder
    '''
    os.chdir(dest_folder)
    for filename in os.listdir(input_folder):
        words = clean_html_text(f'{input_folder}\\{filename}')
        with open(filename[:-5] + '.txt', 'w',encoding = 'utf-8') as file:
            file.write(str(words))
            
                     
            
parser.add_argument("--input_folder", type=str, help='provide a path for the input folder containing html files')
parser.add_argument("--dest_folder", type=str, help='provide a destination folder path')

args = parser.parse_args()


if __name__ == '__main__':
    write_clean_html_text_files(args.input_folder, args.dest_folder) 
