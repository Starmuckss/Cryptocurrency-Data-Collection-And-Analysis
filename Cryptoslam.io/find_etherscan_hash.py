# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 10:55:49 2021

@author: HP
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from datetime import datetime, timedelta
import os
import requests

options = webdriver.FirefoxOptions()
options.headless = True
options.add_argument("--start-maximized")
list_of_links = []

transaction_links = pd.read_pickle("transaction_links2.pkl")


for _,row in transaction_links[150:160].iterrows():
    name = row["SerieName"]
    link = row["transaction_link"]
    
    if link != "":
        b = webdriver.Firefox(options=options) # Bunu sadece bir kere yapsam olur mu
        b.get(link)
        time.sleep(4)
    
    if "etherscan.io" in link:
        try:
            result = b.find_elements_by_xpath("/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[7]/div[2]/ul/div/li[1]/div/a")    
                                                
            e_link = result[0].get_attribute("href")
            list_of_links.append((name,e_link))
        except:
            try:
                result = b.find_elements_by_xpath("/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[7]/div[2]/ul/li/div/a")  
                e_link = result[0].get_attribute("href")
                list_of_links.append((name,e_link))
            except IndexError:
                list_of_links.append((name,""))
    elif "wax.bloks.io" in link:
        try:
            result = b.find_elements_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/div/section[1]/div/table/tbody/tr[7]/td[4]/td/div/div/div/div[1]/div/span")  
                                                
            collection_name = result[0].text
            root_url = "https://wax.bloks.io/account/"
            wax_link = root_url + collection_name
            list_of_links.append((name,wax_link))
        except IndexError:
            list_of_links.append((name,""))
    else:
        list_of_links.append((name,""))
    b.quit()    
df = pd.DataFrame(data = list_of_links)    
df.to_excel("links_for_main_serie_pages.xlsx")
