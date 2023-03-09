from sqlalchemy import insert
from sqlalchemy import text
from config import mssql_get_conn,mssq_datawharehouse
from itertools import chain
import pandas as pd
from tabelas import dim_pedidos_promob
from datetime import date, datetime


def insert_dim_pedido(*args, **kwargs):

    dwengine = mssq_datawharehouse()
    for arg in args:
        print(arg)

        with dwengine.connect() as conn:
                result = conn.execute(insert(dim_pedidos_promob)
                    ,[{"pedido":arg["pedido"],"desc":arg["desc"],"unid":arg["unid"],"nat":int(arg["nat"]),"valor_ab":float(arg["valor_ab"])
                       ,"valor_prod":arg["valor_prod"]
                       ,"valor_un":float(arg["valor_un"]),"quantidade_a":float(arg["quantidade_a"]),"quantidadef":float(arg["quantidadef"])
                       ,"quantidad_s":float(arg["quantidad_s"]),"emissao":arg["emissao"],"entrega":arg["entrega"]
                       ,"oc_pedido":arg["oc_pedido"],"urls":arg["urls"]
                       ,"lote_pedidos":arg["lote_pedidos"],"loja_responsavel":arg["loja_responsavel"],"status_pedidos":arg["status_pedidos"]
                       ,"totais":float(arg["totais"]),"datas_entrega":arg["datas_entrega"],"datas":arg["datas"]
                       ,"cliente_pedidos":arg["cliente_pedidos"],"referencias_pedidos":arg["referencias_pedidos"]}])
                

   