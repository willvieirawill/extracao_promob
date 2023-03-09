from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
import re
from typing import Literal, List, Generator,Any
from itertools import chain, zip_longest
from dotenv import load_dotenv
from urllib import parse
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from inserted import insert_dim_pedido
from datetime import datetime


load_dotenv()


options = webdriver.ChromeOptions() 
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options,
                               executable_path=r"C:\estimadoresteste\extracao_promob\chromedriver\chromedriver.exe")


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
          
          
            a = urls["datas"]
            
            b = urls["dataentrega"]

            dataentrega = datetime.strftime(b, '%d/%m/%Y')

            datasf = datetime.strptime(a, '%d/%m/%Y')
            
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
            dict_items["datas_entrega"] = dataentrega
            dict_items["datas"] = datasf
            dict_items["cliente_pedidos"] = urls["cliente"]
            dict_items["pedido_oc"] = urls["pedidooc"]
            dict_items["referencias_pedidos"] = urls["referenciapedido"]


            insert_dim_pedido(dict_items)
            lista_dicts.append(dict_items)
    
    data = pd.DataFrame(lista_dicts)
    data.to_excel("relatoriopedidosteste.xlsx")

def get_order() -> Generator[dict[str, Any], None, None]:
    """Extrai informações Tela inicial Promob"""
    driver.implicitly_wait(4)
    
    driver.get("https://consultasweb.promob.com/order")
    
    """Seleciona range de datas"""
    data_de = driver.find_element(By.ID,'datepickerinit')
    data_de.clear()
    data_de.send_keys("01/01/2022")


    data_final = driver.find_element(By.ID,'datepickerfin')
    data_final.clear()
    data_final.send_keys("01/02/2023")


    
    time.sleep(1)

    try:
        data_cadastro = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[2]/span')
        datas = [data.text for data in data_cadastro]

    except Exception as e:
        print(e)

    try:
        data_entrega = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[3]/span')
        datas_entrega = [entrega.text for entrega  in data_entrega]
      
    except Exception as e:
        print(e)

    try:
        valortotal = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[11]/div')
        totais = [valor.text.replace(".","").replace(",",".") for valor in valortotal]
      
    except Exception as e:
        print(e)

    try:
        tipos = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[4]')
        tipo_pedidos = [tipo.text for tipo in tipos]

    except Exception as e:
        print(e)
    
    try:
        status = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[5]')
        status_pedidos = [statu.text for statu in status]
     
    except Exception as e:
        print(e)


    try:
        lojas = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[9]')
        loja_responsavel = [loja.text for loja in lojas]
       
    except Exception as e:
        print(e)

    try:
        url_base = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[1]/div/a')
        urls_p = [urls.get_attribute("href") for urls in url_base]
       
    except Exception as e:
        print(e)

    try:
        lotes = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[7]/div')
        lote_pedidos = [lote.text for lote in lotes]
      
    except Exception as e:
        print(e)

    try:
        clientes = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[8]/div')
        cliente_pedidos = [cliente.text for cliente in clientes]
    except Exception as e:
        print(e)

    try:
        oc_pedidos = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[6]')
        pedido_oc = [oc.text for oc in oc_pedidos]
    except Exception as e:
        print(e)

    try:
        refecias_pedidos = driver.find_elements(By.XPATH,'//*[@id="grid"]/tbody/tr/td[1]/div/a')
        referencias_p = [referencias.text for referencias in refecias_pedidos]
    except Exception as e:
        print(e)


    for i in range(len(urls_p)):
        new_dict = {}
        
        try:
            new_dict["urls"] = urls_p[i]
        except:
            pass

        try:
            new_dict["referenciapedido"] = referencias_p[i]
        except:
            pass

        try:
            new_dict["pedidooc"] = pedido_oc[i]
        except:
            pass

        try:
            new_dict["cliente"] = cliente_pedidos[i]
        except:
            pass

        try:
            new_dict["lote"] = lote_pedidos[i]
        except:
            pass

        try:
            new_dict["loja"] = loja_responsavel[i]
        except:
            pass

        try:
            new_dict["status"] = status_pedidos[i]
        except:
            pass

        try:
            new_dict["tipo"] = tipo_pedidos[i]
        except:
            pass

        try:
            new_dict["total"] = totais[i]
        except:
            pass
        try:
            new_dict["dataentrega"] = datas_entrega[i]
        except:
            pass

        new_dict["datas"] = datas[i]
        get_order_detais(new_dict)


 
   
user_login()

get_order()



