import array
from lib2to3.pgen2 import driver
from pickle import FALSE, TRUE
from sqlite3 import Time
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import pickle
import selenium.webdriver
import threading
import matplotlib.pyplot as plt
import numpy as np
import random

open('stockdata.txt','w').close()
Real_email = 'username1'
practise_email = 'username2'
global password
password = 'password'


cookie_xpath  = """//*[@id="__next"]/main/div[3]/div/div[2]/div[2]/div[2]/div[1]/p"""
email_xpath = """//*[@id="__next"]/main/div[3]/div/div[2]/div/div[2]/div/form/div[2]/div/div/input"""
pwd_xpath = """//*[@id="__next"]/main/div[3]/div/div[2]/div/div[2]/div/form/div[3]/div/div/input"""
sign_xpath = """//*[@id="__next"]/main/div[3]/div/div[2]/div/div[2]/div/form/div[5]/input"""
global search_xpath
search_xpath = """//*[@id="app"]/div[3]/div[2]/div[1]/div[1]/div[2]/div/div[1]"""
global currencies_xpath
currencies_xpath = """//*[@id="app"]/div[3]/div[2]/div[2]/div/div[1]/div/div/div/div/div[5]"""
global major_xpath
major_xpath = """//*[@id="app"]/div[3]/div[2]/div[2]/div/div[1]/div/div/div/div/div[5]/div/div[2]/div[1]"""
global xpractise
xpractise = """//*[@id="app"]/div[6]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div[1]"""
global tickers
global ticker_count

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
global Chromedriver
Chromedriver = webdriver.Chrome(options=chrome_options)


Chromedriver.get("https://live.trading212.com/")
Chromedriver.maximize_window()
global practise_driver
practise_driver = webdriver.Chrome(options=chrome_options)
global xpoint
xpoint = np.array([]);
data_set = [0,0]
global stockdata
def xpath_click(driver,click_path):
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, click_path))).click()
   
def xpath_login(driver,find_path, login_info):
    driver.find_element(By.XPATH, find_path).send_keys(login_info)

def text_cleaner():
    element = Chromedriver.find_element(By.CLASS_NAME, """search-results-content""");
    text = element.text
    text = '\n'.join([line for line in text.split('\n') if '%' not in line and '/' not in line and  line.strip() and 'FOREX' not in line and 'Forex' not in line ] )
    text  = '\n'.join([re.sub(r'[^0-9.]', '', line) if re.search(r'[0-9]', line) and re.search(r'[^0-9.\s]', line) else line for line in text.split('\n')])
   
    f = open("stockdata.txt","a")
    f.writelines(text);
    f.close()
    time.sleep(0.2)
    return text
   

def sign_in_sequence(driver, email):
    xpath_click(driver,cookie_xpath)
    xpath_click(driver,email_xpath)
    xpath_login(driver,email_xpath, email)
    xpath_click(driver,pwd_xpath)
    xpath_login(driver,pwd_xpath, password)
    xpath_click(driver,sign_xpath)
   
def real_signin():
    global data_set
    sign_in_sequence(Chromedriver,Real_email);
    time.sleep(60)
    xpath_click(Chromedriver,search_xpath)
    time.sleep(5)
    xpath_click(Chromedriver,currencies_xpath)
    time.sleep(5)
    xpath_click(Chromedriver,major_xpath)
    time.sleep(5)
    tickers = word1 = " ".join(re.findall("[a-zA-Z]+", text_cleaner()))
    ticker_count = len(re.findall("[a-zA-Z]+", text_cleaner()))
    while TRUE:
            data_set = text_cleaner().split('\n')

def practise_signin():
    practise_driver.get("https://live.trading212.com/")
    practise_driver.maximize_window()
    sign_in_sequence(practise_driver,practise_email)
    time.sleep(60)
    xpath_click(practise_driver,xpractise)
'''
def trading_math():
    global stockdata
    stockdata = []
   
    while TRUE:
        time.sleep(1)
        if(data_set[1] != 0):
       
            stockdata.append(float(data_set[1]))
            print(stockdata)
            data_len = len(stockdata);
            xpoints = np.arange(1, data_len + 1, 1).tolist()
            poly = np.polyfit(xpoints, stockdata, deg=12)
            ypoints = np.polyval(poly, xpoints)
            plt.clf()  # Clear the previous plot
            plt.plot(xpoints, stockdata, 'o-', label='Data')  # Plot raw dataufunc 'add' did not contain a loop with signature matching types (dtype('<U7'), dtype('float64')) -> None
            plt.plot(xpoints, ypoints, '--', label='Poly Fit')  # Plot polynomial fit
            plt.legend()
            plt.draw()
            plt.pause(0.01)
'''
       
def trading_math():
    stockdata = []
   
    while True:
        time.sleep(1)
        if data_set[1] != 0:
            stockdata.append(float(data_set[1]))
            print(stockdata)
            data_len = len(stockdata)
            xpoints = np.arange(1, data_len + 1, 1).tolist()

            # Fit a polynomial of degree 12
            poly = np.polyfit(xpoints, stockdata, deg=12)

            # Extrapolate: Add a few more x points beyond the current data
            xpoints_extrapolate = xpoints + [x + 1 for x in xpoints[-3:]]
            ypoints = np.polyval(poly, xpoints_extrapolate)

            plt.clf()  # Clear the previous plot
            plt.plot(xpoints, stockdata, 'o-', label='Data')
            plt.plot(xpoints_extrapolate, ypoints, '--', label='Poly Fit & Extrapolation')
            plt.legend()
            plt.draw()
            plt.pause(0.01)
    return stockdata
threading.Thread(target = real_signin).start()


threading.Thread(target= practise_signin).start()
trading_math();
