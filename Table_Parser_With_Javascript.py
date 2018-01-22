# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 11:38:20 2018

@author: SIVAKUMAR BATTHALA
"""
#%%
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time



#%%
def get_html_data(driver):
    
    html_source = driver.page_source
    
    soup = BeautifulSoup(html_source, 'html.parser')
    soup.findAll('table')[0].findAll('tr')
    
    rows=soup.findAll('table')[1].findAll('tr')
    
    table_contents = []   # store your table here
    for tr in rows:
        if rows.index(tr) == 0 : 
            row_cells = [ th.getText().strip() for th in tr.find_all('th') if th.getText().strip() != '' ]  
        else : 
            row_cells = ([ tr.find('th').getText() ] if tr.find('th') else [] ) + [ td.getText().strip() for td in tr.find_all('td') if td.getText().strip() != '' ] 
        if len(row_cells) > 1 : 
            table_contents += [ row_cells ]
    
    row_headers = table_contents[0]
    tablerows = table_contents[1:]
    return row_headers,tablerows
    
#%%
driver = webdriver.Chrome('C:\\Users\\SIVAKUMAR BATTHALA\\chromedriver.exe')
#%%
url = 'http://mutualfunds.com/themes/commodity-funds/'
driver.get(url)
numpages = 4
delay = 120
driver.implicitly_wait(delay)
WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Next ›')))
appended_data = []
rh,td = get_html_data(driver)
appended_data.append(td)

#%%

for page in range(2, numpages + 1):
    
    
    print(page)
    page_link = driver.find_element_by_link_text(str(page))
    attempts = 0
    while True:
        try:
            page_link.click()
            break
        except: 
            # here I want to refresh/reload the page
            #driver.implicitly_wait(delay)
            time.sleep(delay)
            attempts += 1
            print(attempts)
    
    
    time.sleep(delay)
    rh,td = get_html_data(driver)
    appended_data.append(td)
    
driver.close

flat_list = [item for sublist in appended_data for item in sublist]
df = pd.DataFrame.from_records(flat_list,columns=rh)

#%%
#ignored_exceptions=('NoSuchElementException','StaleElementReferenceException')
    #page_link = WebDriverWait(driver, delay,ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, str(page))))
    #driver.implicitly_wait(delay)
    #WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Next ›')))
    #.send_keys(webdriver.common.keys.Keys.SPACE)
    #page_link = driver.find_element_by_xpath('//div[@class="pagination"]/ol/li/a[text()="%s"]' % page)
#df = pd.concat(appended_data, axis=1)

#url = 'http://mutualfunds.com/themes/commodity-funds/#complete-list&sort_name=net_assets&sort_order=desc&page=1'
#soup = BeautifulSoup(driver.page_source, 'html.parser')
#max_page_element = driver.find_element_by_xpath('//div[@class="pagination"]/ol/li/a')
#max_page = int(max_page_element.text)
 #page_link = driver.find_element_by_link_text('Next ›')
 #driver.execute_script("javascript:void(0)")
    #driver.find_element_by_link_text(str(idx+2)).send_keys(webdriver.common.keys.Keys.SPACE)
    
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, str(idx+2)))).send_keys(webdriver.common.keys.Keys.SPACE)
    #WebDriverWait(driver, delay)
    #time.sleep(delay)from selenium.webdriver.support import expected_conditions
#%%
#def get_web_element_attribute_names(web_element):
#    """Get all attribute names of a web element"""
    # get element html
#    html = web_element.get_attribute("outerHTML")
    # find all with regex
#    pattern = """([a-z]+-?[a-z]+_?)='?"?"""
#    return re.findall(pattern, html)import re