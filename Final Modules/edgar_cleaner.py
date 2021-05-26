# -*- coding: utf-8 -*-
"""
Created on Tue May 25 18:54:49 2021


"""

def clean_html_text(html_text):
    '''
    Takes a html file and returns just the text
    '''
    from bs4 import BeautifulSoup
    with open(html_text, 'r', encoding = 'utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
        soup = soup.getText()
    return soup    
    

def write_clean_html_text_files(input_folder, dest_folder):
    '''
    For each html file in the input folder, get the text and then saves this in destination folder
    '''
    import os
    os.chdir(dest_folder)
    for filename in os.listdir(input_folder):
        words = clean_html_text(f'{input_folder}\\{filename}')
        with open(filename[:-5] + '.txt', 'w',encoding = 'utf-8') as file:
            file.write(str(words))
            
            
write_clean_html_text_files(r"C:\Users\TalinKeoshgerin\Downloads\TESTEROO"\
                            ,r"C:\Users\TalinKeoshgerin\Downloads\TESTEROO2")            
            
