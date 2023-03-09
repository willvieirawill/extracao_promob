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
    driver.get("https://consultasweb.promob.com/Authentication/Index?ReturnUrl")
    driver.implicitly_wait(7)
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


    WebDriverWait(driver, 20).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="div-login"]/div[4]/input'))).click()


    
def get_order_detais(*args, **kwargs) -> None:
    lista_dicts = []
    driver.implicitly_wait(7)
  
    for urls in args:
        print(urls)
        
        driver.get(urls["urls"])
  
        time.sleep(3)

        try:
            emissao = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[3]/span')[0].text
        except Exception as e:
            print(e)

        try:
            entrega = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[4]/span')[0].text
        except Exception as e:
            print(e)
        
        try:
            oc_pedido = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr[1]/td[7]')[0].text
        except Exception as e:
            print(e)
        try:
            quantidade_solicitada = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[6]')
            quantidad_s = [quantidad_s.text.replace(",",".") for quantidad_s in quantidade_solicitada]
        except Exception as e:
            print(e)

        try:
            quantidade_faturada = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[7]/div')
            quantidadef = [quantidadef.text.replace(",",".") for quantidadef in quantidade_faturada]
        except Exception as e:
            print(e)


        try:
            quantidade_em_aberto = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[8]/div')
            quantidade_a = [quantidade_a.text.replace(",",".") for quantidade_a in quantidade_em_aberto]
        except Exception as e:
            print(e)

        try:
            valor_unitario = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[9]/div')
            valor_un = [valor_un.text.replace(",",".") for valor_un in valor_unitario]
        except Exception as e:
            print(e)

        try:
            valor_produtos = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[10]/div')
            valor_prod = [valor_prod.text.replace(",",".") for valor_prod in valor_produtos]
        except Exception as e:
            print(e)

        try:
            valor_aberto = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[11]/div')
            valor_ab = [valor_ab.text.replace(",",".") for valor_ab in valor_aberto]
        except Exception as e:
            print(e)

        try:
            natureza = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[5]')
            nat = [nat.text for nat in natureza]
        except Exception as e:
            print(e)

        try:
            unidade = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[4]')
            unid = [unid.text for unid in unidade]
        except Exception as e:
            print(e)

        try:
            descricao = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[3]')
            desc = [desc.text for desc in descricao]
        except Exception as e:
            print(e)

        try:
            referencias = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[2]')
            refs = [refs.text for refs in referencias]
        except Exception as e:
            print(e)

        try:
            pedidos = driver.find_elements(By.XPATH,'//*[@id="OrderDetail"]/table/tbody/tr/td[1]/div')
            pedido = [pedido.text for pedido in pedidos]
        except Exception as e:
            print(e)

        for i in range(len(pedido)):
            dict_items = {}

       
            dict_items["pedido"] = pedido[i]
            dict_items["refs"] = refs[i]
            dict_items["desc"] = desc[i]
            dict_items["unid"] = unid[i]
            dict_items["nat"] = nat[i]
            dict_items["valor_ab"] = valor_ab[i]
            dict_items["valor_prod"] = valor_prod[i]
            dict_items["valor_un"] = valor_un[i]
            dict_items["quantidade_a"] = quantidade_a[i]
            dict_items["quantidadef"] = quantidadef[i]
            dict_items["quantidad_s"] = quantidad_s[i]

            try:
                dict_items["emissao"] = emissao
            except:
                pass

            try:
                dict_items["entrega"] = entrega
            except:
                pass

            try:
                dict_items["oc_pedido"] = oc_pedido
            except:
                pass

            dict_items["urls"] = urls["urls"]
            dict_items["lote_pedidos"] = urls["lote"]
            dict_items["loja_responsavel"] = urls["loja"]
            dict_items["status_pedidos"] = urls["status"]
            dict_items["tipo_pedidos"] = urls["tipo"]
            dict_items["totais"] = urls["total"]
            dict_items["datas_entrega"] = urls["dataentrega"]
            dict_items["datas"] = urls["datas"]
            dict_items["cliente_pedidos"] = urls["cliente"]
            dict_items["pedido_oc"] = urls["pedidooc"]
            dict_items["referencias_pedidos"] = urls["referenciapedido"]



            lista_dicts.append(dict_items)
    
    data = pd.DataFrame(lista_dicts)
    data.to_csv("relatoriopedidosteste.csv")

def get_order() -> Generator[dict[str, Any], None, None]:
    data = pd.read_csv(r"C:\Users\Mybox Marcenaria\Documents\ETL_rev3\extracao_promob\urlspedidospromob.csv")
    data = data.drop_duplicates()
 
    new_dict = data.to_dict("records")
 
    get_order_detais(*new_dict)
    


   
user_login()

get_order()



