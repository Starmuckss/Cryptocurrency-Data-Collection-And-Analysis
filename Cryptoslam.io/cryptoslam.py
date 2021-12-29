# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 13:43:36 2021

@author: HP
"""
# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import os 
import requests
# specify the url
urlpage = 'https://cryptoslam.io/art-blocks/sales' 
# urlpage ='https://groceries.asda.com/search/yogurt'
print(urlpage)

dir_path = os.path.dirname(os.path.realpath(__file__))

# https://github.com/mozilla/geckodriver/releases download geckodriver here
# run firefox webdriver from executable path of your choice
# give where you extracted your geckodriver as parameter


# page = urllib.request.urlopen(urlpage)
# soup = BeautifulSoup(page, 'html.parser')
# for tr in (soup.findAll("table"))[1]: 
#     try:
#         for td in tr.find_all("td"):
#             print(td.text)
#     except:
#         continue
# print('Number of results', len(results))
driver = webdriver.Firefox(executable_path=dir_path+"\\geckodriver.exe")

driver.get(urlpage)
# execute script to scroll down the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 30s
time.sleep(30)
# driver.quit()
# "/html/body/div[2]/div/div[4]/div/div/div/div[3]/div[1]/div[3]/div/table/tbody" works gives table as string
results = driver.find_elements_by_xpath("/html/body/div[2]/div/div[4]/div/div/div/div[3]/div[1]/div[3]/div/table/tbody/tr")
print('Number of results', len(results))

# create empty array to store data
data = []
# loop over results
for result in results:
    # product_name = result.text
    print(result.text)
    # link = result.find_element_by_tag_name('a')
    # product_link = link.get_attribute("href")
    # # append dict to array
    # data.append({"product" : product_name, "link" : product_link})
    

# close driver 
driver.quit()
# save to pandas dataframe
df = pd.DataFrame(data)
print(df)    
# write to csv
df.to_csv('asdaYogurtLink.csv')