from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
import re
from dotenv import load_dotenv
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from datetime import datetime

load_dotenv()


options = webdriver.ChromeOptions() 
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
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

def inform_date():
    driver.implicitly_wait(7)
    try:
        data_de = driver.find_element(By.ID,'datepickerinit')
        data_de.clear()
        data_de.send_keys("01/01/2021")
    except Exception as e:
        print(e)

    try:
        data_ate = driver.find_element(By.ID,'datepickerfin')
        data_ate.clear()
        data_ate.send_keys("02/01/2023")
    except Exception as e:
        print(e)

    time.sleep(3)

    try:
        confirm = driver.find_element(
            By.CSS_SELECTOR,'#OrderGrid > div.k-header.k-grid-toolbar.k-grid-top > a.toolbar-refresh.k-icon.k-button.k-button-icontext')
        confirm.click()
    except Exception as e:
        print(e)


def delete_cache():
    driver.execute_script("window.open('');")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    driver.get('chrome://settings/clearBrowserData') # for old chromedriver versions use cleardriverData
    time.sleep(2)
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3)
    actions.perform()
    time.sleep(2)
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * 4 + Keys.ENTER)
    actions.perform()
    time.sleep(5)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def unselect():
    driver.implicitly_wait(7)
    try:
        child_3 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#type > div > input[type=checkbox]:nth-child(3)')))
        child_3.click()
    except Exception as e:
        print(e)


    try:
        cbSale = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cbSale')))
        cbSale.click()
    except Exception as e:
        print(e)


    try:
        child = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#type > div > input[type=checkbox]:nth-child(2)')))
        child.click()
    except Exception as e:
        print(e)

    try:
        cbAll = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#status > div > label:nth-child(3) > input[type=checkbox]')))
        cbAll.click()
    except Exception as e:
        print(e)

    try:
        realizado = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#status > div > label:nth-child(5) > input[type=checkbox]')))
        realizado.click()
    except Exception as e:
        print(e)


    inform_date()


def user_login() -> None:
    driver.get("https://consultasweb.promob.com/Authentication/Index?ReturnUrl")
    driver.implicitly_wait(7)
    time.sleep(4)

    empresa = driver.find_element(By.ID, "company")
    ActionChains(driver)\
        .send_keys_to_element(
        empresa, "HR")\
        .perform()

    usuario = driver.find_element(
        By.ID, "username")
    ActionChains(driver)\
        .send_keys_to_element(
        usuario, "MYBOXFRANQUIA")\
        .perform()

    password = driver.find_element(
        By.ID, "password-clear")
    ActionChains(driver)\
        .send_keys_to_element(
        password, "mybox")\
        .perform()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="div-login"]/div[4]/input'))).click()

def get_urls():
    driver.implicitly_wait(7)
    lista_dicts = []
    driver.get("https://consultasweb.promob.com/order")
    time.sleep(5)
  
    unselect()
    time.sleep(7)

    scroll_page()
    try:
        urls_order = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[1]/div/a')
        for urls in urls_order:
            print(urls.get_attribute("href"))
            dict_new_url = {
                "UrlPedido":urls.get_attribute("href")}
            print(urls.get_attribute("href"))
            lista_dicts.append(dict_new_url)
           
            
    except Exception as e:
        print(e)
    '''
    try:
        data_emissao = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[2]/span')
        for data in data_emissao:
            print(data.text)
    except Exception as e:
        print(e)

    try:
        ordem_compra = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[6]')
        for ordem in ordem_compra:
            print(ordem.text)
    except Exception as e:
        print(e)

    try:
        valor_total = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[11]/div')
        for val in valor_total:
            print(val.text)
    except Exception as e:
        print(e)


    '''
    try:
        data = pd.DataFrame(lista_dicts)
        print(data)
        data.to_csv("urls1703.csv")
    except:
        pass
    
def get_items():
    lista_dicts = []
    driver.implicitly_wait(7)
    data = pd.read_csv(r"C:\Users\Mybox Marcenaria\Documents\ETL_rev3\extracao_promob\urls1703.csv",sep=";")

    listas = data.UrlPedido.to_list()
    for lista in listas:
        dict_items = {}
        driver.get(lista)
        time.sleep(1)

        scroll_page()

        try:
            pedido = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[2]/div')[0].text
            dict_items["Pedido"] = pedido
        except Exception as e:
            print(e)
    
        try:
            emissao = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[3]/span')[0].text
            dict_items["DataEmissao"] =emissao
        except Exception as e:
            print(e)
        
        try:
            d_entrega = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[4]/span')[0].text
            dict_items["DataEntrega"] =d_entrega
        except Exception as e:
            print(e)
        
        try:
            tipo = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[5]')[0].text
            dict_items["Tipo"] =tipo
        except Exception as e:
            print(e)
        try:
            status = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[2]/div')[0].text
            dict_items["Status"] =status
        except Exception as e:
            print(e)
        
        try:
            lote = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[6]')[0].text
            dict_items["Lote"] = lote
        except Exception as e:
            print(e)
        
        try:
            cliente_cod = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[9]/div')[0].text
            dict_items["Codigocliente"] = cliente_cod
        except Exception as e:
            print(e)
        
        try:
            nome_cliente =driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[10]')[0].text
            dict_items["NomeCliente"] = nome_cliente
        except Exception as e:
            print(e)

        try:
            transportadora = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[11]')[0].text
            dict_items["Transportadora"] =transportadora
        except Exception as e:
            print(e)

        try:
            v_total = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[12]/div')[0].text
            dict_items["ValorTotal"] = v_total
        except Exception as e:
            print(e)

        try:
            items = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody')
            new_item = [item.text.split("\n") for item in items]
         
        except Exception as e:
            print(e)
        lista_dicts.append(new_item)

        print(new_item)
        print(lista)
    

user_login()
delete_cache()
user_login()
get_items()
#get_urls()


#extract_referencias()




