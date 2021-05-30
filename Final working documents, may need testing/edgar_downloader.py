import requests,re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


#import argparse

#parser = argparse.ArgumentParser(description='demo of command line argument parsing')

headers = {"User-Agent": r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

def requests_retry_session(
    retries=5,
    backoff_factor=0.3
):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def write_page(url, file_path): 
    '''
    Opens url and writes html to the file path
    '''
    with open(file_path, 'w',  encoding='utf-8') as file:
        response = requests_retry_session().get(url, headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')
        file.write(str(soup))

def new_downloader(ticker):
    sec_website = "https://www.sec.gov/"
    browse_url = sec_website + "cgi-bin/browse-edgar"
    requests_params = {'action': 'getcompany',
            'CIK': ticker.upper(),
            'type': '10-K',
            'datea': 20180101,
            'dateb': 20210530,
            'owner': 'exclude',
            'output': 'html'}
    headers = {"User-Agent": r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    linkList = []
    listy = {}
    continuation_tag = 'first pass'

    while continuation_tag:
        r = requests_retry_session().get(browse_url, params=requests_params,headers=headers)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        for link in soup.find_all('a', {'id': 'documentsbutton'}):
            URL = sec_website + link['href']
            linkList.append(URL)
        continuation_tag = soup.find('input', {'value': 'Next ' + str(100)}) # a button labelled 'Next 100' for example
        if continuation_tag:
            continuation_string = continuation_tag['onclick']
            browse_url = sec_website + re.findall('cgi-bin.*count=\d*', continuation_string)[0]
            requests_params = None
    
    for URL in linkList:
        close = requests_retry_session().get(URL, headers=headers)
        soupy = BeautifulSoup(close.text, "html.parser")
        date = soupy.find_all('class' == 'formGrouping')[0].find_all('class'=='info')[0]
        date = re.findall(r'\d\d\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}', str(date))[0]
        ''' cant get this to work, did long way round
        row = soupy.find_all('tr')[1].find_all('td')[2]
        listy.append(row['href'])'''
        value = soupy.find_all('tr')[1].find_all('td')[2]
        values = re.findall(r'"([^"]*)"', str(value))[1]
        values = re.sub(r"/ix\?doc=", '', values)
        listy[sec_website + values] = date
    return(listy)

def download_files_10k(ticker,dest_folder):
    '''
    Changes directory to destination folder. Calls the selenium to get a link, date dictionary. Uses these to   write the html to the file name.
    '''
    os.chdir(dest_folder)
    for tick in ticker :
        urls= new_downloader(tick)
        print(f'Saving html for {tick}')

        for key,value in urls.items(): 
            print('saving to folder')
            write_page(key, f'{tick}_10-K_{value}.html')
            time.sleep(1)
    print('complete')



#parser.add_argument("--ticker_list", default='AAPL,MSFT', type=str, help='provide a list of tickers seperated by , e.g. "MSFT,AAPL"')
#parser.add_argument("--dest_folder", type=str, help='provide a destination folder path')

#args = parser.parse_args()

#so args.ticker_list is a string
#tl = str(args.ticker_list).split(',')


#if __name__ == '__main__':
    #download_files_10k(tl, args.dest_folder)
    

