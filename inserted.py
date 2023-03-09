from sqlalchemy import insert
from sqlalchemy import text
from config import mssql_get_conn,mssq_datawharehouse
from itertools import chain
import pandas as pd
from tabelas import dim_pedidos_promob



def insert_dim_pedido(*args, **kwargs):
    dwengine = mssq_datawharehouse()
    for arg in args:
        print(arg)
       
        with dwengine.connect() as conn:
                result = conn.execute(insert(dim_pedidos_promob)
                    ,[{"ref_pedido":arg["pedido"],"Nomes":arg["Nomes"],"quantidadesolicitada":arg["quantidadesolicitada"]
                       ,"quantidadefaturada":arg["quantidadefaturada"]
                     ,"quantidadeemaberto":arg["quantidadeemaberto"]
                    ,"valorunitario":arg["valorunitario"],"valorprodutos":arg["valorprodutos"],"referenciaprodutos":arg["referenciaprodutos"]
                    ,"unidade":arg["unidade"]
                    ,"ncm":arg["ncm"],"urls":arg["urls"]
                     ,"lote_pedidos":arg["lote_pedidos"],"status_pedidos":arg["status_pedidos"]
                     ,"tipo_pedidos":arg["tipo_pedidos"]
                    ,"totais":arg["totais"],"datas_entrega":arg["datas_entrega"],
                     "datas":arg["datas"],"cliente_pedidos":arg["cliente_pedidos"]
                     ,"pedido_oc":arg["oc_pedido"],"referencias_pedidos":arg["referencias_pedidos"]}])
                

