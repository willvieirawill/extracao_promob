from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
import re
from typing import Literal, List, Generator,Any
from dotenv import load_dotenv
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from inserted import insert_dim_pedido
from datetime import datetime
from dateutil import parser

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
    driver.implicitly_wait(7)
    driver.get("https://consultasweb.promob.com/Authentication/Index?ReturnUrl")
    
    time.sleep(4)

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
    
    time.sleep(7)
    try:
       element= driver.find_element(By.XPATH,'#div-login > div:nth-child(5) > input').click()
    except:
        print("error")

    avancar = driver.find_element(By.CSS_SELECTOR, '#div-login > div:nth-child(5) > input')
    actions = ActionChains(driver)
    actions.click(avancar)
    actions.perform()

    time.sleep(20)
  
   

def get_urls(*args, **kwargs):
    lista_dicts = []
    driver.implicitly_wait(7)
    driver.get("https://consultasweb.promob.com/order")

    try:
        data_de = driver.find_element(By.ID,'datepickerinit')
        data_de.clear()
        data_de.send_keys('01/01/2020')
    except:
        print("erro")

    try:
        data_ate = driver.find_element(By.ID,'datepickerfin')
        data_ate.clear()
        data_ate.send_keys('12/03/2023')
    except:
        print("erro")


    try:
        clicar = driver.find_element(
            By.CSS_SELECTOR,'#OrderGrid > div.k-header.k-grid-toolbar.k-grid-top > a.toolbar-refresh.k-icon.k-button.k-button-icontext')
        actions = ActionChains(driver)
        actions.click(clicar)
        actions.perform()
    except:
        pass


    try:
        liberado = driver.find_element(
            By.CSS_SELECTOR,'#status > div > label:nth-child(3) > input[type=checkbox]')
        actions = ActionChains(driver)
        actions.click(clicar)
        actions.perform()
    except:
        pass

    time.sleep(1)
    try:
        tliberado = driver.find_element(
            By.CSS_SELECTOR,'#status > div > label:nth-child(5) > input[type=checkbox]')
        actions = ActionChains(driver)
        actions.click(clicar)
        actions.perform()
    except:
        pass


    try:
        total = driver.find_element(
            By.CSS_SELECTOR,'#cbAll')
        actions = ActionChains(driver)
        actions.click(clicar)
        actions.perform()
    except:
        pass


    time.sleep(7)



def get_orders():
    lista_urls = []
    get_urls()
    driver.implicitly_wait(7)

    time.sleep(3)

    scroll_page()
  
    urls_pedidos = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[1]/div/a')
    for urls in urls_pedidos:
        urls_pedidos = {}
        urls_pedidos['urls'] = urls.get_attribute("href")
        print(urls_pedidos)
        lista_urls.append(urls_pedidos)
    data = pd.DataFrame(lista_urls)
    data.to_excel("urls_orders.xlsx")


#user_login()

#get_orders()

def extract_item():
    driver.implicitly_wait(7)
    data = pd.read_excel(r"C:\Users\Mybox Marcenaria\Documents\ETL_rev3\extracao_promob\urls_orders.xlsx")
    new_dict = data.to_dict("records")
    for item in new_dict:
        
        driver.get(item['urls'])
       
        try:
            informacoes = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td/div')
          
            #for informacao in informacoes:
            #    print(informacao.text)
        except:
            pass
            
        try:
            cliente_fantasia = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[10]')[0].text
            print(cliente_fantasia)
        except:
            print("error")


        try:
            transp_fantasia = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[11]')[0].text
            print(transp_fantasia)
        except:
            print("error")

        try:
            valor_total = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[12]/div')[0].text
            print(valor_total)
        except:
            print("error")


user_login()
#extract_item()
     
