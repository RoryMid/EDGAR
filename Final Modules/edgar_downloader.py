import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

#import argparse

#parser = argparse.ArgumentParser(description='demo of command line argument parsing')

headers = {"User-Agent": r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

def write_page(url, file_path): 
    '''
    Opens url and writes html to the file path
    '''
    with open(file_path, 'w',  encoding='utf-8') as file:
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')
        file.write(str(soup))

def selenium_activate(key):
    '''
    Selenium gets to a page with a table of 10-k filings. Saves the (cleaned) links with their date. 
    Returns dictionary or URL and Date.
    '''
    driver = webdriver.Chrome()
    print('loading up website')

    driver.get('https://www.sec.gov/edgar/searchedgar/companysearch.html')

    xpath_search = r'/html/body/div[2]/div/div/div/section/div[3]/div[2]/div[2]/div[3]/div/form/input[1]'
    driver.find_element_by_xpath(xpath_search).click()

    searchinput_path = r'/html/body/div[2]/div/div/div/section/div[3]/div[2]/div[2]/div[3]/div/form/input[1]'
    driver.find_element_by_xpath(searchinput_path).send_keys(key, Keys.ENTER)

    w = WebDriverWait(driver,30)
    w.until(expected_conditions.element_to_be_clickable((By.XPATH, r'/html/body/main/div[4]/div[2]/div[3]/h5')))
    button1 = driver.find_element_by_xpath(r'/html/body/main/div[4]/div[2]/div[3]/h5')
    button1.click()

    w.until(expected_conditions.element_to_be_clickable((By.XPATH, r'/html/body/main/div[4]/div[2]/div[3]/div/button[1]')))
    button2 = driver.find_element_by_xpath(r'/html/body/main/div[4]/div[2]/div[3]/div/button[1]')
    button2.click()

    w.until(expected_conditions.element_to_be_clickable((By.XPATH, r'/html/body/main/div[5]/div/div[1]/div[1]/div/input[3]')))
    xpath_search1 = r'/html/body/main/div[5]/div/div[1]/div[1]/div/input[3]'
    driver.find_element_by_xpath(xpath_search1).click()

    searchinput_path1 = r'/html/body/main/div[5]/div/div[1]/div[1]/div/input[3]'
    driver.find_element_by_xpath(searchinput_path1).clear()

    w.until(expected_conditions.element_to_be_clickable((By.XPATH, r'/html/body/main/div[5]/div/div[1]/div[1]/div/input[2]')))
    xpath_search = r'/html/body/main/div[5]/div/div[1]/div[1]/div/input[2]'
    driver.find_element_by_xpath(xpath_search).click()

    searchinput_path = r'/html/body/main/div[5]/div/div[1]/div[1]/div/input[2]'
    driver.find_element_by_xpath(searchinput_path).send_keys('10-K', Keys.ENTER)

    print('getting urls')
    time.sleep(2)

    url = {}
    import re
    for row in driver.find_elements_by_css_selector("tr.odd"):
        for cell in row.find_elements_by_class_name("document-link"):
            x = cell.get_attribute("href")
            #import re
            x = re.sub(r"/ix\?doc=", '', x)
            time.sleep(1)
        y = row.find_elements_by_tag_name("td")[2].text
        time.sleep(1)
        url[x] = y
    
    for row in driver.find_elements_by_css_selector("tr.even"):
        for cell in row.find_elements_by_class_name("document-link"):
            x = cell.get_attribute("href")
            #import re
            x = re.sub(r"/ix\?doc=", '', x)
            time.sleep(1)
        y = row.find_elements_by_tag_name("td")[2].text
        time.sleep(1)
        url[x] = y

    print('urls gathered, chrome closing')
    driver.quit()
    return url


def download_files_10k(ticker,dest_folder):
    '''
    Changes directory to destination folder. Calls the selenium to get a link, date dictionary. Uses these to   write the html to the file name.
    '''
    os.chdir(dest_folder)
    for tick in ticker:
        urls= selenium_activate(tick)
        print('Saving html')

        for key,value in urls.items(): 
            write_page(key, f'{tick}_10-K_{value}.html')
            time.sleep(1)
    print('complete')



#parser.add_argument("--ticker_list", default='AAPL,MSFT', type=str, help='provide a list of tickers seperated by , e.g. "MSFT,AAPL"')
#parser.add_argument("--dest_folder", type=str, help='provide a destination folder path')

#args = parser.parse_args()

#so args.ticker_list is a string
#tl = str(args.ticker_list).split(',')


if __name__ == '__main__':
    download_files_10k(tl, args.dest_folder)
    

