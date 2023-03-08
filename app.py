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
import re

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


    WebDriverWait(driver, 20).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="div-login"]/div[4]/input'))).click()


def get_order_detais(*args, **kwargs) -> None:
    
    driver.implicitly_wait(7)
    lista_dicts = []
    for urls in args:
        print(urls)
        dict_items = {}

        driver.get(urls["URLS"])

        time.sleep(3)
      
        scroll_page()

        referencias = driver.find_elements(By.XPATH,'//*[@id="grid"]/thead/tr/th/span')
        refs = [referencia.text for referencia in referencias]

        valores = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td')
        val = [valor.text for valor in valores if valor]
        new_item  = list(filter(None, val))

        new_dict = dict(zip_longest(refs, new_item))

        valores_2 = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr')
        order = [orders.text.split("\n") for orders in valores_2]
        for i in range(len(order)):
            
       
            dict_items['URLS'] = urls["URLS"]
            dict_items['LOJAS'] = urls["LOJAS"]
            dict_items['REFERENCIAS'] = urls["REFERENCIAS"]
            dict_items['LOTES'] = urls["LOTES"]
            dict_items['DATACADASTRO'] = urls["DATACADASTRO"]
            dict_items['DATAENTREGA'] = urls["DATAENTREGA"]
            dict_items['VALOR'] = urls["VALOR"]
            dict_items['TIPO'] = urls["TIPO"]
            dict_items['STATUS'] = urls["STATUS"]
      

            #dict_items["ReferenciaPedido"] = order_url.split("=")[-1]

            try:
                dict_items['Pedidos'] = order[i][0]
                dict_items['Nomes'] = order[i][1]
                dict_items['Quantidade Solicitada'] = order[i][2]
                dict_items['Quantidade Faturada'] = order[i][3]
                dict_items['Quantidade Faturada'] = order[i][4]
                dict_items['Quantidade em aberto'] = order[i][5]
                dict_items['Valor unitario'] = order[i][6]
                dict_items['Valor Produtos'] = order[i][7]
               
                dict_items.update(new_dict)
                
            except Exception as e:
                print(e)
            
           
        lista_dicts.append(dict_items)
    data = pd.DataFrame(lista_dicts)
    data.to_excel("pedidosteste.xlsx")
 

def get_order() -> Generator[dict[str, Any], None, None]:
    
    driver.implicitly_wait(4)
    
    driver.get("https://consultasweb.promob.com/order")
    

    data_de = driver.find_element(By.ID,'datepickerinit')
    data_de.clear()
    data_de.send_keys("01/01/2022")


    data_final = driver.find_element(By.ID,'datepickerfin')
    data_final.clear()
    data_final.send_keys("01/02/2023")

    time.sleep(3)

    scroll_page()
    lista_datas = []
    lista_entrega = []
    lista_valor = []
    lista_tipo = []
    lista_status = []
    lista_lojas = []
    lista_urls = []
    lista_referencias = []
    lista_lotes = []

    try:
        data_cadastro = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[2]/span')
        for datas in data_cadastro:
            lista_datas.append(datas.text)
    except Exception as e:
        print(e)


    try:
        data_entrega = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[3]/span')
        for entregas in data_entrega:
            lista_entrega.append(entregas.text)
    except Exception as e:
        print(e)

    
    try:
        valortotal = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[11]/div')
        for valores in valortotal:
            lista_tipo.append(valores.text)
    except Exception as e:
        print(e)

    try:
        tipo = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[4]')
        for tipos in tipo:
            lista_valor.append(tipos.text)
    except Exception as e:
        print(e)
    

    try:
        status = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[5]')
        for statu in status:
            lista_status.append(statu.text)
    except Exception as e:
        print(e)



    try:
        lojas = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[9]')
        for loja in lojas:
            lista_lojas.append(loja.text)
    except Exception as e:
        print(e)

    try:
        url_base = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[1]/div/a')
        for urls in url_base:
            lista_urls.append(urls.get_attribute("href"))
            lista_referencias.append(urls.text)
 
    except Exception as e:
        print(e)

    try:
        lotes = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[7]/div')
        for lote in lotes:
            lista_lotes.append(lote.text)
          
    except Exception as e:
        print(e)
    

    for i in range(len(lista_urls)):
        new_dict = {}
        try:
            new_dict["URLS"] = lista_urls[i]
            new_dict["DATACADASTRO"] = lista_datas[i]
            new_dict["DATAENTREGA"] = lista_entrega[i]
            new_dict["TIPO"] = lista_valor[i]
            new_dict["VALOR"] = lista_tipo[i]
            new_dict["STATUS"] = lista_status[i]
            new_dict["LOJAS"] = lista_lojas[i]
            new_dict["URLS"] = lista_urls[i]
            new_dict["REFERENCIAS"] = lista_referencias[i]
            new_dict["LOTES"] = lista_lotes[i]
          
            get_order_detais(new_dict)
        except Exception as e:
            print(e)
        #get_order_detais


user_login()

get_order()



