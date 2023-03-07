from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
import re
from typing import Literal, List, Generator
from itertools import chain, zip_longest
from pathlib import Path
from dotenv import load_dotenv
from urllib import parse
from dotenv import load_dotenv
from os import path
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from typing import Generator, Any
import pandas as pd

load_dotenv()



options = webdriver.ChromeOptions() 
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options,
                               executable_path=r"C:\Users\Mybox Marcenaria\Documents\ETL_rev3\extracao_promob\chromedriver\chromedriver.exe")


def scroll_page() -> None:
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(1)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

def user_login() -> None:
    driver.get("https://consultasweb.promob.com/Authentication/Index?ReturnUrl")
    driver.implicitly_wait(7)
    time.sleep(4)
    #password = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'password-clearr'))).click()
    #password.clear()

    empresa = driver.find_element(By.ID, "company")
    ActionChains(driver)\
        .send_keys_to_element(empresa, "HR")\
        .perform()

    usuario = driver.find_element(By.ID, "username")
    ActionChains(driver)\
        .send_keys_to_element(usuario, "MYBOXFRANQUIA")\
        .perform()

    password = driver.find_element(By.ID, "password-clear")
    ActionChains(driver)\
        .send_keys_to_element(password, "mybox")\
        .perform()


    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="div-login"]/div[4]/input'))).click()


def get_order() -> Generator[dict[str, Any], None, None]:
    driver.get("https://consultasweb.promob.com/order")
    driver.implicitly_wait(7)

    data_de = driver.find_element(By.ID,'datepickerinit')
    data_de.clear()
    data_de.send_keys("01/01/2022")


    data_final = driver.find_element(By.ID,'datepickerfin')
    data_final.clear()
    data_final.send_keys("01/02/2023")


    scroll_page()
    try:
        orders = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[1]/div/a')
        orders = [order.get_attribute("href") for order in orders]
        yield orders
    except Exception as e:
        print(e)


def get_order_detais() -> None:
    driver.implicitly_wait(7)

    orders = get_order()
    get_oder = [order for order in chain.from_iterable(orders)]
    for order in get_oder:
        time.sleep(1)
        driver.get(order)
        time.sleep(3)
        dict_item = {}

        scroll_page()

        try:
            headers = driver.find_elements(By.XPATH,'//*[@id="grid"]/thead/tr/th')
            valores = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td')
            cont = 0
            for header in headers:
                dict_item[header.get_attribute('data-field')] = valores[cont].text
                cont +=1
                
        except Exception as e:
            print(e)
     

        try:
            attrs = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/thead/tr/th')
            val = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td')
            cont = 0
            for att in attrs:
                dict_item[att.get_attribute("data-title")] = val[cont].text
                cont +=1
             
        except Exception as e:
            print(e)


   

        print(dict_item)




#get_order_detais()

def teste():
    driver.implicitly_wait(7)
    driver.get("https://consultasweb.promob.com/orderitems?orderid=235121")
    dict_item = {}

    scroll_page()
    
  
  
    
    OrderDetail = driver.find_elements(By.ID,'OrderDetail')
    orders = [orders.text.split("\n") for orders in chain.from_iterable(OrderDetail)]

    fields_orders = ['Pedido', 'Item Cód', 'Item Descrição', 'UN', 'Natureza', 'Qtde Solicitada',
                      'Qtde Faturada', 'Qtde Aberto', 'Vl Unit', 'Vl Produtos', 'Vl Prod Aberto']
    #items = driver.find_elements(By.CLASS_NAME,'k-master-row')


    data = pd.DataFrame(orders, columns=fields_orders)
    print(data)
 


user_login()
dict_item = teste()
